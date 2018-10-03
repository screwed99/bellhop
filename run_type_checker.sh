#!/bin/bash
source activate bellhop
mypy --config-file mypy.ini .
