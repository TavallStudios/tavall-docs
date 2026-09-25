#!/bin/sh
set -eu
python3 --version
python3 scripts/ci/test_verify_docs.py
python3 scripts/ci/verify_docs.py --mode build
python3 scripts/ci/verify_docs.py --mode integration
