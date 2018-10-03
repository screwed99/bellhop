#!/bin/bash
set -e
source activate bellhop
./run_type_checker.sh
python main.py "$@"
