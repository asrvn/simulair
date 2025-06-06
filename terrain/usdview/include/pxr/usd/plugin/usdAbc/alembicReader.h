#line 1 "/builds/omniverse/usd-ci/USD/pxr/usd/plugin/usdAbc/alembicReader.h"
//
// Copyright 2016 Pixar
//
// Licensed under the terms set forth in the LICENSE.txt file available at
// https://openusd.org/license.
//
#ifndef PXR_USD_PLUGIN_USD_ABC_ALEMBIC_READER_H
#define PXR_USD_PLUGIN_USD_ABC_ALEMBIC_READER_H

/// \file usdAbc/alembicReader.h

#include "pxr/pxr.h"
#include "pxr/usd/sdf/abstractData.h"
#include "pxr/usd/sdf/fileFormat.h"
#include "pxr/base/tf/token.h"
#include <memory>
#include <stdint.h>
#include <string>
#include <vector>

PXR_NAMESPACE_OPEN_SCOPE


// Note -- Even though this header is private we try to keep Alembic headers
//         out of it anyway for simplicity's sake.

/// \class UsdAbc_AlembicDataReader
///
/// An alembic reader suitable for an SdfAbstractData.
///
class UsdAbc_AlembicDataReader {
public:
    typedef int64_t Index;

    UsdAbc_AlembicDataReader();
    UsdAbc_AlembicDataReader (const UsdAbc_AlembicDataReader&) = delete;
    UsdAbc_AlembicDataReader& operator= (const UsdAbc_AlembicDataReader&) = delete;
    ~UsdAbc_AlembicDataReader();

    /// Open a file.  Returns \c true on success;  errors are reported by
    /// \c GetErrors().
    bool Open(const std::string& filePath, 
              const SdfFileFormat::FileFormatArguments&);

    /// Close the file.
    void Close();

    /// Return any errors.
    std::string GetErrors() const;

    /// Set a reader flag.
    void SetFlag(const TfToken&, bool set = true);

    /// Test for the existence of a spec at \p path.
    bool HasSpec(const SdfPath& path) const;

    /// Returns the spec type for the spec at \p path.
    SdfSpecType GetSpecType(const SdfPath& path) const;

    /// Test for the existence of and optionally return the value at
    /// (\p path,\p fieldName).
    bool HasField(const SdfPath& path,
                  const TfToken& fieldName,
                  SdfAbstractDataValue* value) const;

    /// Test for the existence of and optionally return the value at
    /// (\p path,\p fieldName).
    bool HasField(const SdfPath& path,
                  const TfToken& fieldName,
                  VtValue* value) const;

    /// Test for the existence of and optionally return the value of the
    /// property at \p path at index \p index.
    bool HasValue(const SdfPath& path, Index index,
                  SdfAbstractDataValue* value) const;

    /// Test for the existence of and optionally return the value of the
    /// property at \p path at index \p index.
    bool HasValue(const SdfPath& path, Index index,
                  VtValue* value) const;

    /// Visit the specs.
    void VisitSpecs(const SdfAbstractData& owner,
                    SdfAbstractDataSpecVisitor* visitor) const;

    /// List the fields.
    TfTokenVector List(const SdfPath& path) const;

    /// The type holds a set of Usd times and can return an Alembic index
    /// for each time.
    class TimeSamples {
        typedef std::vector<double> _UsdTimeCodes;
    public:
        typedef _UsdTimeCodes::const_iterator const_iterator;

        /// Construct an empty set of samples.
        TimeSamples();

        /// Construct from the time samples which must be monotonically
        /// increasing.
        TimeSamples(const std::vector<double>& times);

        /// Swaps the contents of this with \p other.
        void Swap(TimeSamples& other);

        /// Returns \c true iff there are no samples.
        bool IsEmpty() const;

        /// Returns the number of samples.
        size_t GetSize() const;

        /// Returns the Usd times.
        std::set<double> GetTimes() const;

        /// Returns the time sample at index \p index.
        double operator[](size_t index) const;

        /// Add these Usd times to the given set.
        void AddTo(std::set<double>*) const;

        /// Returns the index for Usd time \p usdTime and returns \c true
        /// or returns \c false if \p usdTime is not in the set of samples.
        bool FindIndex(double usdTime, Index* index) const;

        /// Returns the times bracketing \p time.
        bool Bracket(double usdTime, double* tLower, double* tUpper) const;

        /// Returns the times bracketing \p time.
        template <class T>
        static bool Bracket(const T&, double usdTime,
                            double* tLower, double* tUpper);

    private:
        // The monotonically increasing Usd times.
        _UsdTimeCodes _times;
    };

    /// Returns the sampled times over all properties.
    const std::set<double>& ListAllTimeSamples() const;

    /// Returns the sampled times for the property at \p path.
    const TimeSamples& 
    ListTimeSamplesForPath(const SdfPath& path) const;

private:
    std::unique_ptr<class UsdAbc_AlembicDataReaderImpl> _impl;
    std::string _errorLog;
};


PXR_NAMESPACE_CLOSE_SCOPE

#endif
