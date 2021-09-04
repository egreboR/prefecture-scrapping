#!/bin/bash

echo $1 2>> '/home/data/$1.log'

touch '/home/data/$1.log'
python3 './web-scrapping/$1.py' 2>> '/home/data/$1.log'

