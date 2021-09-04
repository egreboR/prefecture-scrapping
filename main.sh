#!/bin/bash

touch '/home/data/$1.log'
echo $1 2>> '/home/data/$1.log'
echo $CWD 2>> '/home/data/$1.log'
echo 'TEST' 2>> '/home/data/$1.log'
python3 './$1.py' 2>> '/home/data/$1.log'

