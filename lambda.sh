#!/bin/sh

# How to bundle the source code for an AWS Lambda Function including the installation of external dependencies

# Required: apt-get install python3-venv
# 1) External dependencies
#virtualenv v-env
python3 -m venv v-env
#source v-env/bin/activate
pip install -r requirements.txt
deactivate

cd v-env/lib/python3.6/site-packages
zip -r9 ${OLDPWD}/dependencies.zip .

cd $OLDPWD
# Clean-up
rm -r v-env

# 2) Source code from repository
cp dependencies.zip src/prediction.zip
cd src
zip -g -r prediction.zip model/ utils/ prediction_handler.py
cd ..
mv src/prediction.zip .


