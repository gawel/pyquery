#!/bin/bash
# script to run selenium tests

# get geckodriver
./tests/geckodriver.sh

# run tox with py3.7
MOZ_HEADLESS=1 PATH=$PATH:$PWD tox -e py37 tests/test_real_browser.py
