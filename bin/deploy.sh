#!/bin/bash

main() {

    log "change to project root"
    cd $(git rev-parse --show-toplevel)

    environment
    build
}


environment() {
    log "setup python environment"
    python3 -m venv build-env

    log "activating environment"
    source  build-env/bin/activate

    log "installing twine -the pypi helper"
    pip install twine

    log "we might need wheel"
    pip install wheel
}

build() {
    log "build python dist"
    python setup.py sdist bdist_wheel upload
}

clean() {
    deactivate
    rm -rf build-env
    rm -rf build
    rm -rf dist
    rm -rf simplerr.egg-info
}

# Utilities
log() {
    printf "\n👉 $*\n"
}


main
