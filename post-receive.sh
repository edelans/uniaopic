#!/bin/bash
#This script is exectuted by the post-receive hook
#it contains commands that must be executed when code is pulled

# some colors
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo  "\n${YELLOW}##########################################${NC}"
echo  "${YELLOW}#    Exectution post-receive.sh script   #${NC}"
echo  "${YELLOW}##########################################${NC}"

# activate virtual env
echo  "\n\n${YELLOW}activate virtual env${NC}"
. ~/.virtualenvs/uniaopic/bin/activate

# install new requirements with pip
echo "\n\n${YELLOW}install new requirements with pip (quiet mode)${NC}"
pip install -r requirements.txt -q

# restart app
echo "\n\n${YELLOW}restart app${NC}"
sudo systemctl restart uniaopic
