# No hashbang - should be sourced

this_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd -P)"

if [ -f "${this_dir}/set_usd_python_env.sh" ]; then
    source "${this_dir}/set_usd_python_env.sh"
fi

export USD_INSTALL_DIR="$(dirname "${this_dir}")"

export PATH="$USD_INSTALL_DIR/bin${PATH:+:${PATH}}"
if [[ $(uname) == MINGW64* ]]; then
    export PATH="$USD_INSTALL_DIR/lib:$USD_INSTALL_DIR/plugin/usd${PATH:+:${PATH}}"
    export PYTHONPATH="$(cygpath -w "$USD_INSTALL_DIR/lib/python")${PYTHONPATH:+;${PYTHONPATH}}"
else
    export LD_LIBRARY_PATH="$USD_INSTALL_DIR/lib:$USD_INSTALL_DIR/plugin/usd${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
    export PYTHONPATH="$USD_INSTALL_DIR/lib/python:$USD_PYTHON_DEPS_DIR${PYTHONPATH:+:${PYTHONPATH}}"
fi

built_with_asan_support="0"

if [ "$built_with_asan_support" != "0" ]; then
    asan_path="$USD_INSTALL_DIR/lib/libasan.so.4"
    if [ -f "$asan_path" ]; then
        export LD_PRELOAD="${asan_path}${LD_PRELOAD:+:${LD_PRELOAD}}"
        echo "USD has been built with Address Sanitizers. libasan added to LD_PRELOAD"

        # ASan enables memory leak detection by default but causes lots of errors with boost python
        # LSan should be used to track down memory leaks
        if [[ -z "${ASAN_OPTIONS}" ]]; then
            export ASAN_OPTIONS="detect_leaks=0"
        else
            echo "WARN: ASAN_OPTIONS has been set, make sure detect_leaks=0 to prevent numerous boost python errors"
        fi
    else
        echo "ERROR: USD has been built with Address Sanitizers, but unable to find libasan at ${asan_path}"
        exit 1
    fi
fi

built_with_tsan_support="0"

if [ "$built_with_tsan_support" != "0" ]; then
    tsan_path="$USD_INSTALL_DIR/lib/libtsan.so.0"
    if [ -f "$tsan_path" ]; then
        export LD_PRELOAD="${tsan_path}${LD_PRELOAD:+:${LD_PRELOAD}}"
        echo "USD has been built with Thread Sanitizers. libtsan added to LD_PRELOAD"
    else
        echo "ERROR: USD has been built with Thread Sanitizers, but unable to find libtsan at ${tsan_path}"
        exit 1
    fi
fi

export PXR_MTLX_STDLIB_SEARCH_PATHS="$USD_INSTALL_DIR/libraries"

echo "Activated USD python/tools from" $USD_INSTALL_DIR
