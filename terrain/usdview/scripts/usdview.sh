#!/bin/bash

set -e
THIS_DIR="$(cd "$(dirname ${BASH_SOURCE[0]})" && pwd)"
. "${THIS_DIR}/set_usd_env.sh"

"${USD_INSTALL_DIR}/bin/usdview" "$@"

