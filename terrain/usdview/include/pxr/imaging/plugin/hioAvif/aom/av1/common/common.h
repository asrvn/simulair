#line 1 "/builds/omniverse/usd-ci/USD/pxr/imaging/plugin/hioAvif/aom/av1/common/common.h"
/*
 * Copyright (c) 2016, Alliance for Open Media. All rights reserved
 *
 * This source code is subject to the terms of the BSD 2 Clause License and
 * the Alliance for Open Media Patent License 1.0. If the BSD 2 Clause License
 * was not distributed with this source code in the LICENSE file, you can
 * obtain it at www.aomedia.org/license/software. If the Alliance for Open
 * Media Patent License 1.0 was not distributed with this source code in the
 * PATENTS file, you can obtain it at www.aomedia.org/license/patent.
 */

#ifndef AOM_AV1_COMMON_COMMON_H_
#define AOM_AV1_COMMON_COMMON_H_

/* Interface header for common constant data structures and lookup tables */

#include <assert.h>

#include "pxr/imaging/plugin/hioAvif/aom/aom_dsp/aom_dsp_common.h"
#include "pxr/imaging/plugin/hioAvif/aom/aom_mem/aom_mem.h"
#include "pxr/imaging/plugin/hioAvif/aom/aom_integer.h"
#include "pxr/imaging/plugin/hioAvif/aom/aom_ports/bitops.h"
#include "pxr/imaging/plugin/hioAvif/aom/config/aom_config.h"

#ifdef __cplusplus
extern "C" {
#endif

#define PI 3.141592653589793238462643383279502884

// Only need this for fixed-size arrays, for structs just assign.
#define av1_copy(dest, src)              \
  {                                      \
    assert(sizeof(dest) == sizeof(src)); \
    memcpy(dest, src, sizeof(src));      \
  }

// Use this for variably-sized arrays.
#define av1_copy_array(dest, src, n)           \
  {                                            \
    assert(sizeof(*(dest)) == sizeof(*(src))); \
    memcpy(dest, src, n * sizeof(*(src)));     \
  }

#define av1_zero(dest) memset(&(dest), 0, sizeof(dest))
#define av1_zero_array(dest, n) memset(dest, 0, n * sizeof(*(dest)))

static INLINE int get_unsigned_bits(unsigned int num_values) {
  return num_values > 0 ? get_msb(num_values) + 1 : 0;
}

#define CHECK_MEM_ERROR(cm, lval, expr) \
  AOM_CHECK_MEM_ERROR(&cm->error, lval, expr)

#define AOM_FRAME_MARKER 0x2

#define AV1_MIN_TILE_SIZE_BYTES 1

#ifdef __cplusplus
}  // extern "C"
#endif

#endif  // AOM_AV1_COMMON_COMMON_H_
