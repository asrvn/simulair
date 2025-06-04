#!/bin/bash -e

this_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd)"

source "${this_dir}/set_usd_env.sh"

if [ $# -eq 0 ]; then
    usdview "${USD_INSTALL_DIR}/share/usd/tutorials/traversingStage/HelloWorld.usda"
else
    usdview $@
fi