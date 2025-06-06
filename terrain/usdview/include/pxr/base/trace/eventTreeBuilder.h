#line 1 "/builds/omniverse/usd-ci/USD/pxr/base/trace/eventTreeBuilder.h"
//
// Copyright 2018 Pixar
//
// Licensed under the terms set forth in the LICENSE.txt file available at
// https://openusd.org/license.
//

#ifndef PXR_BASE_TRACE_EVENT_TREE_BUILDER_H
#define PXR_BASE_TRACE_EVENT_TREE_BUILDER_H

#include "pxr/pxr.h"

#include "pxr/base/trace/collection.h"
#include "pxr/base/trace/counterAccumulator.h"
#include "pxr/base/trace/eventNode.h"
#include "pxr/base/trace/eventTree.h"

PXR_NAMESPACE_OPEN_SCOPE

///////////////////////////////////////////////////////////////////////////////
///
/// \class Trace_EventTreeBuilder
///
/// This class creates a tree of TraceEventTree instances from
/// TraceCollection instances.
///
class Trace_EventTreeBuilder
    : protected TraceCollection::Visitor {
public:
    /// Constructor.
    Trace_EventTreeBuilder();

    /// Returns the created tree.
    TraceEventTreeRefPtr GetTree() { return _tree; }

    /// Creates a TraceEventTree from the data in /p collection.
    TRACE_API void CreateTree(const TraceCollection& collection);

    /// Set the value of the counters.
    void SetCounterValues(
        const TraceEventTree::CounterMap& counterValues) {
        _counterAccum.SetCurrentValues(counterValues);
    }

protected:
    /// \name TraceCollection::Visitor Interface
    /// @{
    virtual void OnBeginCollection() override;
    virtual void OnEndCollection() override;
    virtual bool AcceptsCategory(TraceCategoryId) override;
    virtual void OnBeginThread(const TraceThreadId&) override;
    virtual void OnEndThread(const TraceThreadId&) override;
    virtual void OnEvent(
        const TraceThreadId&, const TfToken&, const TraceEvent&) override;
    /// @}

private:

    // Helper class for event graph creation.
    struct _PendingEventNode {
        using TimeStamp = TraceEvent::TimeStamp;

        struct AttributeData {
            TimeStamp time;
            TfToken key;
            TraceEventNode::AttributeData data;
        };

        _PendingEventNode( const TfToken& key, 
                                 TraceCategoryId category,
                                 TimeStamp start,
                                 TimeStamp end,
                                 bool separateEvents,
                                 bool isComplete);
        TraceEventNodeRefPtr Close();

        // Can move this, but not copy it
        _PendingEventNode(const _PendingEventNode&) = delete;
        _PendingEventNode& operator= (const _PendingEventNode&) = delete;

        _PendingEventNode(_PendingEventNode&&) = default;
        _PendingEventNode& operator= (_PendingEventNode&&) = default;

        TfToken key;
        TraceCategoryId category;
        TimeStamp start;
        TimeStamp end;
        bool separateEvents;
        bool isComplete;
        std::vector<TraceEventNodeRefPtr> children;
        std::vector<AttributeData> attributes;
    };

    void _OnBegin(const TraceThreadId&, const TfToken&, const TraceEvent&);
    void _OnEnd(const TraceThreadId&, const TfToken&, const TraceEvent&);
    void _OnData(const TraceThreadId&, const TfToken&, const TraceEvent&);
    void _OnTimespan(const TraceThreadId&, const TfToken&, const TraceEvent&);
    void _OnMarker(const TraceThreadId&, const TfToken&, const TraceEvent&);

    using _PendingNodeStack = std::vector<_PendingEventNode>;
    using _ThreadStackMap = std::map<TraceThreadId, _PendingNodeStack>;

    void _PopAndClose(_PendingNodeStack& stack); 

    TraceEventNodeRefPtr _root;
    _ThreadStackMap _threadStacks;
    TraceEventTreeRefPtr _tree;

    class _CounterAccumulator : public TraceCounterAccumulator {
    protected:
        bool _AcceptsCategory(TraceCategoryId) override;
    };
    _CounterAccumulator _counterAccum;

    TraceEventTree::MarkerValuesMap _markersMap;
};

PXR_NAMESPACE_CLOSE_SCOPE

#endif // PXR_BASE_TRACE_EVENT_TREE_BUILDER_H