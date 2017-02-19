#!/bin/bash

set -e

virtualenv .
source bin/activate
pip install -r requirements.txt

python -m unittest discover

cd ./zappa_deploy
bash ./zappa_deploy.sh
cd ..
zappa update $1