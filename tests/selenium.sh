#!/bin/bash
# script to run selenium tests

driver="https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz"

# get geckodriver
[ -f geckodriver ] || wget -cqO- $driver | tar xvzf -

# run tox with py3.6
MOZ_HEADLESS=1 PATH=$PATH:$PWD tox -e py36 tests/test_real_browser.py
