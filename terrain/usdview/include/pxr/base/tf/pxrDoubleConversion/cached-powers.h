#line 1 "/builds/omniverse/usd-ci/USD/pxr/base/tf/pxrDoubleConversion/cached-powers.h"
// Copyright 2010 the V8 project authors. All rights reserved.
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
//       notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
//       copyright notice, this list of conditions and the following
//       disclaimer in the documentation and/or other materials provided
//       with the distribution.
//     * Neither the name of Google Inc. nor the names of its
//       contributors may be used to endorse or promote products derived
//       from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#ifndef DOUBLE_CONVERSION_CACHED_POWERS_H_
#define DOUBLE_CONVERSION_CACHED_POWERS_H_

#include "diy-fp.h"

#include "pxr/pxr.h"

PXR_NAMESPACE_OPEN_SCOPE

namespace pxr_double_conversion {

namespace PowersOfTenCache {

  // Not all powers of ten are cached. The decimal exponent of two neighboring
  // cached numbers will differ by kDecimalExponentDistance.
  static const int kDecimalExponentDistance = 8;

  static const int kMinDecimalExponent = -348;
  static const int kMaxDecimalExponent = 340;

  // Returns a cached power-of-ten with a binary exponent in the range
  // [min_exponent; max_exponent] (boundaries included).
  void GetCachedPowerForBinaryExponentRange(int min_exponent,
                                            int max_exponent,
                                            DiyFp* power,
                                            int* decimal_exponent);

  // Returns a cached power of ten x ~= 10^k such that
  //   k <= decimal_exponent < k + kCachedPowersDecimalDistance.
  // The given decimal_exponent must satisfy
  //   kMinDecimalExponent <= requested_exponent, and
  //   requested_exponent < kMaxDecimalExponent + kDecimalExponentDistance.
  void GetCachedPowerForDecimalExponent(int requested_exponent,
                                        DiyFp* power,
                                        int* found_exponent);

}  // namespace PowersOfTenCache

}  // namespace pxr_double_conversion

PXR_NAMESPACE_CLOSE_SCOPE

#endif  // DOUBLE_CONVERSION_CACHED_POWERS_H_
