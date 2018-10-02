#!/bin/bash
source activate bellhop
python -m unittest discover --pattern="*_tests.py"
