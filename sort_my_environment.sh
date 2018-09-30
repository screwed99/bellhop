#!/bin/bash

ENV_EXISTS=`conda env list | grep -c bellhop`

if [ $ENV_EXISTS ]; then
{
	echo "Updating environment"
	conda env update -n bellhop -f requirements.txt
}
else
{
	echo "Setting up environment for first time"
	conda env create -f requirements.txt
}
fi

echo "Activate your environment now with: conda activate bellhop"
