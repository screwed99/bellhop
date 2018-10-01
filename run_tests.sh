#!/bin/bash
conda env create -f requirements.txt
source activate bellhop
python -m unittest discover --pattern="*_tests.py"
