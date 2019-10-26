#!/bin/bash

driver="https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz"

[ -f geckodriver ] || wget -cqO- $driver | tar xvzf -
