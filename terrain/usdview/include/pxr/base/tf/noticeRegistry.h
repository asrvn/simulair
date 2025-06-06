#line 1 "/builds/omniverse/usd-ci/USD/pxr/base/tf/noticeRegistry.h"
//
// Copyright 2016 Pixar
//
// Licensed under the terms set forth in the LICENSE.txt file available at
// https://openusd.org/license.
//
#ifndef PXR_BASE_TF_NOTICE_REGISTRY_H
#define PXR_BASE_TF_NOTICE_REGISTRY_H

/// \file tf/noticeRegistry.h
/// \ingroup group_tf_Notification

#include "pxr/pxr.h"
#include "pxr/base/tf/api.h"
#include "pxr/base/tf/hash.h"
#include "pxr/base/tf/hashmap.h"
#include "pxr/base/tf/hashset.h"
#include "pxr/base/tf/notice.h"
#include "pxr/base/tf/singleton.h"
#include "pxr/base/tf/type.h"

#include <tbb/enumerable_thread_specific.h>
#include <tbb/spin_mutex.h>
#include <atomic>

PXR_NAMESPACE_OPEN_SCOPE

/// \class Tf_NoticeRegistry
/// \ingroup group_tf_Notification
/// \internal
///
/// Internal class representing the singleton notification registry.
///
/// Implementation notes.
///
/// The registry is maintained as a hash map that carries TfNotice class to a
/// list of call back entries (each of type \c TfNotice::_DelivererBase*).
///
/// Currently, each list has a mutex which is used for getting/setting the
/// head of the list.  When an item on the list needs to be removed (either
/// from a TfNotice::Revoke() call or because the listening object has
/// expired), the item is removed from the list IF nobody else is using the
/// registry.
///
/// Otherwise, the item is left as an inactive item on the list; at some
/// point, we should maintain a free-list of items that need pruning, and
/// remove them when the registry's user count indicates it is not being used.
/// This is left to do: but note that items should accumulate slowly in the
/// registry, since multiple active traversals (either by different threads,
/// or because of reentrancy) should be rare.
///
class Tf_NoticeRegistry {
    Tf_NoticeRegistry(const Tf_NoticeRegistry&) = delete;
    Tf_NoticeRegistry& operator=(const Tf_NoticeRegistry&) = delete;
public:
    void _BeginDelivery(const TfNotice &notice,
                        const TfWeakBase *sender,
                        const std::type_info &senderType,
                        const TfWeakBase *listener,
                        const std::type_info &listenerType,
                        const std::vector<TfNotice::WeakProbePtr> &probes);

    void _EndDelivery(const std::vector<TfNotice::WeakProbePtr> &probes);
    
    // Register a particular deliverer, return the key created for the
    // registration.
    TfNotice::Key _Register(TfNotice::_DelivererBase* deliverer);

    // Send notice n to all interested listeners.
    size_t _Send(const TfNotice &n, const TfType &noticeType,
                 const TfWeakBase *s, const void *senderUniqueId,
                 const std::type_info &senderType);

    // Remove listener instance indicated by \p key.  This is pass by
    // reference so we can mark the key as having been revoked.  If
    // \p wait is true then don't return while any thread is invoking
    // the handler.
    void _Revoke(TfNotice::Key& key, bool wait = false);

    // Abort if casting of a notice failed; warn if it succeeded but
    // TfSafeDynamic_cast was required.
    void _VerifyFailedCast(const std::type_info& toType,
                           const TfNotice& notice, const TfNotice* castNotice);
    
    // Return reference to singleton object.
    static Tf_NoticeRegistry& _GetInstance() {
        return TfSingleton<Tf_NoticeRegistry>::GetInstance();
    }

    void _InsertProbe(const TfNotice::WeakProbePtr &probe);
    void _RemoveProbe(const TfNotice::WeakProbePtr &probe);

    void _IncrementBlockCount();
    void _DecrementBlockCount();

private:
    Tf_NoticeRegistry();
    friend class TfSingleton<Tf_NoticeRegistry>;

    void _BadTypeFatalMsg(const TfType& t, const std::type_info&);

    typedef TfNotice::_DelivererList _DelivererList;

    typedef std::pair<_DelivererList*, _DelivererList::iterator>
        _DelivererListEntry;

    typedef tbb::spin_mutex _Mutex;
    typedef tbb::spin_mutex::scoped_lock _Lock;

    void _BeginSend(const TfNotice &notice,
                    const TfWeakBase *sender,
                    const std::type_info &senderType,
                    const std::vector<TfNotice::WeakProbePtr> &probes);
    void _EndSend(const std::vector<TfNotice::WeakProbePtr> &probes);

    // It is safe to add a new item onto an STL list during traversal by
    // multiple threads; the only thing to guard against is a race when
    // setting/getting the head of the list.
    //
    // Removal is trickier: if we can remove something right away, we do (i.e.
    // if nobody but us is traversing the registry).  Otherwise, we just mark
    // the item on the list as inactive.

    class _DelivererContainer {
    public:
        typedef TfHashMap<const TfWeakBase*, _DelivererList, TfHash>
            _PerSenderTable;

        _Mutex _mutex;
        _DelivererList _delivererList;
        _PerSenderTable _perSenderTable;

        // Initialize _perSenderTable with zero buckets
        _DelivererContainer() : _perSenderTable(0) {}
    };

    typedef TfHashMap<TfType, _DelivererContainer*, TfHash> _DelivererTable;

    typedef TfHashSet<TfNotice::WeakProbePtr, TfHash> _ProbeTable;

    void
    _Prepend(_DelivererContainer*c, const TfWeakBase* sender,
             TfNotice::_DelivererBase* item) {
        _Lock lock(c->_mutex);

        TF_DEV_AXIOM(!item->_list);

        _DelivererList *dlist;
        if (sender)
            dlist = &c->_perSenderTable[sender];
        else
            dlist = &c->_delivererList;

        item->_list = dlist;
        item->_list->push_front(item);
        item->_listIter = dlist->begin();
    }

    _DelivererListEntry
    _GetHead(_DelivererContainer* c) {
        _Lock lock(c->_mutex);
        return _DelivererListEntry(&c->_delivererList,
                                   c->_delivererList.begin());
    }

    _DelivererListEntry
    _GetHeadForSender(_DelivererContainer* c, const TfWeakBase* s) {
        _Lock lock(c->_mutex);
        _DelivererContainer::_PerSenderTable::iterator i =
            c->_perSenderTable.find(s);
        if (i != c->_perSenderTable.end()) {
            return _DelivererListEntry(&(i->second), i->second.begin());
        } else {
            return _DelivererListEntry((_DelivererList*) 0,
                                       _DelivererList::iterator());
        }
    }

    _DelivererContainer* _GetDelivererContainer(const TfType& t) {
        _Lock lock(_tableMutex);
        _DelivererTable::iterator i = _delivererTable.find(t);
        return (i == _delivererTable.end()) ? NULL : i->second;
    }
    
    _DelivererContainer* _GetOrCreateDelivererContainer(const TfType& t) {
        _Lock lock(_tableMutex);    
        _DelivererTable::iterator i = _delivererTable.find(t);

        if (i == _delivererTable.end())
            return (_delivererTable[t] = new _DelivererContainer);
        else
            return i->second;
    }

    int _Deliver(const TfNotice &n, const TfType &type,
                 const TfWeakBase *s,
                 const void *senderUniqueId,
                 const std::type_info &senderType,
                 const std::vector<TfNotice::WeakProbePtr> &probes,
                 const _DelivererListEntry & entry);
    void _FreeDeliverer(const TfNotice::_DelivererWeakPtr & d);

    void _IncrementUserCount(int amount) {
        _Lock lock(_userCountMutex);
        _userCount += amount;
    }

    _DelivererTable _delivererTable;
    _Mutex _tableMutex;

    // The user count and mutex track the number of callers into the registry
    // to determine when it is safe to remove entries from deliverer lists;
    // entries cannot be removed if another thread is inserting or iterating 
    // over the list at the same time. The mutex is also used to protect
    // access to _deadEntries; these entries will be discarded later, but
    // only when the user count is 1.
    _Mutex _userCountMutex;
    int _userCount;
    std::vector< TfNotice::_DelivererWeakPtr > _deadEntries;

    _Mutex _warnMutex;
    TfHashSet<std::string, TfHash> _warnedBadCastTypes;
    
    _Mutex _probeMutex;
    _ProbeTable _probes;
    bool _doProbing;

    std::atomic<size_t> _globalBlockCount;
    tbb::enumerable_thread_specific<size_t> _perThreadBlockCount;
};

PXR_NAMESPACE_CLOSE_SCOPE

#endif // PXR_BASE_TF_NOTICE_REGISTRY_H
