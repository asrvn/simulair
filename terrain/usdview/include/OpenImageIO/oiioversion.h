// Copyright 2008-present Contributors to the OpenImageIO project.
// SPDX-License-Identifier: BSD-3-Clause
// https://github.com/OpenImageIO/oiio


#ifndef OPENIMAGEIO_VERSION_H
#define OPENIMAGEIO_VERSION_H


// Versioning of the OpenImageIO software. For *releases*:
//
// MAJOR is a major architectural change or a step that does not preserve
// backwards compatibility of source code (an app designed for an older
// major version may not compile successfully against newer version of the
// headers and libraries, and will need to have its source modified).
// Examples of changes that necessitate major version changes are removal of
// API calls or classes, or renaming of class members.
//
// MINOR is an addition of significant new features and may change the
// definition of public data structures or functions in a way that is
// backwards compatible for source code, but is not back compatible for ABI
// or linkage (i.e. you don't need to modify your app's source, but you do
// need to recompile it). Examples of changes that necessitate a minor
// version change would be adding new data fields to a structure, adding new
// virtual member functions to a class, or adding new optional parameters to
// the end of a function call.
//
// PATCH is a minor change that preserves ABI and link back-compatibility,
// where an app built for the older version can simply have the newer
// library substituted without recompilation. Generally, this is only for
// bug fixes, though sometimes we may add new minor features if they only
// involve addition of static/global function calls or data (since this does
// not break back-compatibility).
//
// TWEAK is just a rebuild/re-version that is both forward and backward
// compatible. Usually this involves only a change to the build system
// itself (such as fixing a build break on a particular platform), a change
// in documentation, or fixing some other minor unintentional flaw in a
// prior release.
//
// Note that these designations only apply to released branches. Changes
// in the main development branch ("master") do not make any compatibility
// guarantees at all.
//
#define OIIO_VERSION_MAJOR 2
#define OIIO_VERSION_MINOR 3
#define OIIO_VERSION_PATCH 21
#define OIIO_VERSION_TWEAK 0
#define OIIO_VERSION_RELEASE_TYPE 

// Construct a single integer version number from major, minor, patch.
// Example of its use:
//
//     #if OIIO_VERSION >= OIIO_MAKE_VERSION(2,3,0)
//         ... use a feature introduced in version 2.3.0 ...
//     #endif
//
#define OIIO_MAKE_VERSION(major,minor,patch) \
                        (10000 * (major) + 100 * (minor) + (patch))

// Single version designation of this release
#define OIIO_VERSION OIIO_MAKE_VERSION(OIIO_VERSION_MAJOR, \
                        OIIO_VERSION_MINOR, OIIO_VERSION_PATCH)

// Test if OIIO is >= a particular version.
#define OIIO_VERSION_GREATER_EQUAL(major,minor,patch) \
                        OIIO_VERSION >= OIIO_MAKE_VERSION(major,minor,patch)

// Test if OIIO is < a particular version.
#define OIIO_VERSION_LESS(major,minor,patch) \
                        OIIO_VERSION < OIIO_MAKE_VERSION(major,minor,patch)

// We also define the old name for backwards compatibility purposes.
#define OPENIMAGEIO_VERSION OIIO_VERSION

// Magic macros to make OIIO_VERSION_STRING that looks like "1.2.3"
#define OIIO_MAKE_VERSION_STRING2(a,b,c,d) #a "." #b "." #c #d
#define OIIO_MAKE_VERSION_STRING(a,b,c,d) OIIO_MAKE_VERSION_STRING2(a,b,c,d)
#define OIIO_VERSION_STRING \
    OIIO_MAKE_VERSION_STRING(OIIO_VERSION_MAJOR, \
                             OIIO_VERSION_MINOR, OIIO_VERSION_PATCH, \
                             OIIO_VERSION_RELEASE_TYPE)
#define OIIO_INTRO_STRING "OpenImageIO " OIIO_VERSION_STRING " http://www.openimageio.org"

// Only major.minor.patch.tweak, omit any release type
#define OIIO_VERSION_STRING_MMPT \
    OIIO_MAKE_VERSION_STRING(OIIO_VERSION_MAJOR, \
                             OIIO_VERSION_MINOR, OIIO_VERSION_PATCH, \
                             OIIO_VERSION_TWEAK, "")


// Establish the name spaces
namespace OpenImageIO_v2_3 { }
namespace OIIO = OpenImageIO_v2_3;

// Macros to use in each file to enter and exit the right name spaces.
#define OIIO_NAMESPACE OpenImageIO_v2_3
#define OIIO_NAMESPACE_STRING "OpenImageIO_v2_3"
#define OIIO_NAMESPACE_BEGIN namespace OpenImageIO_v2_3 {
#define OIIO_NAMESPACE_END }
#define OIIO_NAMESPACE_USING using namespace OIIO;


/// Each imageio DSO/DLL should include this statement:
///      DLLPUBLIC int FORMAT_imageio_version = OPENIMAGEIO_PLUGIN_VERSION;
/// libOpenImageIO will check for compatibility this way.
/// This should get bumped any time we change the API in any way that
/// will make previously-compiled plugins break.
///
/// History:
/// Version 3 added supports_rectangles() and write_rectangle() to
/// ImageOutput, and added stride parameters to the ImageInput read
/// routines.
/// Version 10 represents forking from NVIDIA's open source version,
/// with which we break backwards compatibility.
/// Version 11 teased apart subimage versus miplevel specification in
/// the APIs and per-channel formats (introduced in OIIO 0.9).
/// Version 12 added read_scanlines(), write_scanlines(), read_tiles(),
///     write_tiles(), and ImageInput::supports(). (OIIO 1.0)
/// Version 13 added ImageInput::valid_file().  (OIIO 1.1)
/// Version 14 added ImageOutput::open() variety for multiple subimages.
/// Version 15 added support for "deep" images (changing ImageSpec,
///     ImageInput, ImageOutput).
/// Version 16 changed the ImageInput functions taking channel ranges
///     from firstchan,nchans to chbegin,chend.
/// Version 17 changed to int supports(string_view) rather than
///     bool supports(const std::string&)). (OIIO 1.6)
/// Version 18 changed to add an m_threads member to ImageInput/Output.
/// Version 19 changed the definition of DeepData.
/// Version 20 added FMT_imageio_library_version() to plugins. (OIIO 1.7)
/// Version 21 changed the signatures of ImageInput methods: added
///     subimage,miplevel params to many read_*() methods; changed thread
///     safety expectations; removed newspec param from seek_subimage;
///     added spec(subimage,miplevel) and spec_dimensions(subimage,miplevel).
///     (OIIO 2.0)
/// Version 22 changed the signatures of ImageInput/ImageOutput create()
///     to return unique_ptr. (OIIO 2.0)
/// Version 23 added set_ioproxy() methods to ImageInput & ImageOutput
///     (OIIO 2.2).
/// Version 24 Added a PIMPL pointers to ImageInput and ImageOutput and
///     removed some unnecessary fields that were exposed.
/// Version 25 added the thumbnail retrieval and set. (OIIO 2.3)

#define OIIO_PLUGIN_VERSION 25

#define OIIO_PLUGIN_NAMESPACE_BEGIN OIIO_NAMESPACE_BEGIN
#define OIIO_PLUGIN_NAMESPACE_END OIIO_NAMESPACE_END

#ifdef EMBED_PLUGINS
#define OIIO_PLUGIN_EXPORTS_BEGIN
#define OIIO_PLUGIN_EXPORTS_END
#else
#define OIIO_PLUGIN_EXPORTS_BEGIN extern "C" {
#define OIIO_PLUGIN_EXPORTS_END }
#endif

// Which CPP standard (11, 14, etc.) was this copy of OIIO *built* with?
#define OIIO_BUILD_CPP 14

// DEPRECATED(2.1): old macros separately giving compatibility.
#define OIIO_BUILD_CPP11 (14 >= 11)
#define OIIO_BUILD_CPP14 (14 >= 14)
#define OIIO_BUILD_CPP17 (14 >= 17)
#define OIIO_BUILD_CPP20 (14 >= 20)

#endif

