#!/bin/bash

driver="https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz"

[ -f geckodriver ] || wget -cqO- $driver | tar xvzf -
