//
// Copyright 2024 Pixar
// Licensed under the terms set forth in the LICENSE.txt file available at
// https://openusd.org/license.
//
//  (C) Copyright R.W. Grosse-Kunstleve 2002.
//  Distributed under the Boost Software License, Version 1.0. (See
//  accompanying file LICENSE_1_0.txt or copy at
//  http://www.boost.org/LICENSE_1_0.txt)
#ifndef PXR_EXTERNAL_BOOST_PYTHON_OBJECT_PICKLE_SUPPORT_HPP
# define PXR_EXTERNAL_BOOST_PYTHON_OBJECT_PICKLE_SUPPORT_HPP

#include "pxr/pxr.h"
#include "pxr/external/boost/python/common.hpp"

#ifndef PXR_USE_INTERNAL_BOOST_PYTHON
#include <boost/python/object/pickle_support.hpp>
#else

# include "pxr/external/boost/python/detail/prefix.hpp"

namespace PXR_BOOST_NAMESPACE { namespace python {

namespace api
{
  class object;
}
using api::object;
class tuple;

PXR_BOOST_PYTHON_DECL object const& make_instance_reduce_function();

struct pickle_suite;

namespace error_messages {

  template <class T>
  struct missing_pickle_suite_function_or_incorrect_signature {};

  inline void must_be_derived_from_pickle_suite(pickle_suite const&) {}
}

namespace detail { struct pickle_suite_registration; }

struct pickle_suite
{
  private:
    struct inaccessible {};
    friend struct detail::pickle_suite_registration;
  public:
    static inaccessible* getinitargs() { return 0; }
    static inaccessible* getstate() { return 0; }
    static inaccessible* setstate() { return 0; }
    static bool getstate_manages_dict() { return false; }
};

namespace detail {

  struct pickle_suite_registration
  {
    typedef pickle_suite::inaccessible inaccessible;

    template <class Class_, class Tgetinitargs>
    static
    void
    register_(
      Class_& cl,
      tuple (*getinitargs_fn)(Tgetinitargs),
      inaccessible* (* /*getstate_fn*/)(),
      inaccessible* (* /*setstate_fn*/)(),
      bool)
    {
      cl.enable_pickling_(false);
      cl.def("__getinitargs__", getinitargs_fn);
    }

    template <class Class_,
              class Rgetstate, class Tgetstate,
              class Tsetstate, class Ttuple>
    static
    void
    register_(
      Class_& cl,
      inaccessible* (* /*getinitargs_fn*/)(),
      Rgetstate (*getstate_fn)(Tgetstate),
      void (*setstate_fn)(Tsetstate, Ttuple),
      bool getstate_manages_dict)
    {
      cl.enable_pickling_(getstate_manages_dict);
      cl.def("__getstate__", getstate_fn);
      cl.def("__setstate__", setstate_fn);
    }

    template <class Class_,
              class Tgetinitargs,
              class Rgetstate, class Tgetstate,
              class Tsetstate, class Ttuple>
    static
    void
    register_(
      Class_& cl,
      tuple (*getinitargs_fn)(Tgetinitargs),
      Rgetstate (*getstate_fn)(Tgetstate),
      void (*setstate_fn)(Tsetstate, Ttuple),
      bool getstate_manages_dict)
    {
      cl.enable_pickling_(getstate_manages_dict);
      cl.def("__getinitargs__", getinitargs_fn);
      cl.def("__getstate__", getstate_fn);
      cl.def("__setstate__", setstate_fn);
    }

    template <class Class_>
    static
    void
    register_(
      Class_&,
      ...)
    {
      [[maybe_unused]] typedef typename
        error_messages::missing_pickle_suite_function_or_incorrect_signature<
          Class_>::error_type error_type;
    }
  };

  template <typename PickleSuiteType>
  struct pickle_suite_finalize
  : PickleSuiteType,
    pickle_suite_registration
  {};

} // namespace detail

}} // namespace PXR_BOOST_NAMESPACE::python

#endif // PXR_USE_INTERNAL_BOOST_PYTHON
#endif // PXR_EXTERNAL_BOOST_PYTHON_OBJECT_PICKLE_SUPPORT_HPP
