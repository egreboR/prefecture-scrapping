
#!/bin/bash

export PATH='${PATH}:/home/'
touch '/home/data/${1}.log'
python3 './web-scrapping/${1}.py' 2>> '/home/data/${1}.log'

