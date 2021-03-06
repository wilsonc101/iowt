#!/bin/bash

ENV_LIBS="/home/chris/.virtualenvs/iowt-www/lib/python3.5/site-packages"
APP="/home/chris/dev/iowt/www/iowt-www"
ZIP_FILE="/home/chris/iowt-www.zip"


rm $ZIP_FILE

zip -9 $ZIP_FILE

cd $ENV_LIBS
zip -9 -r --exclude=*.pyc* $ZIP_FILE .


cd $APP
zip -g $ZIP_FILE app.py
#zip -g $ZIP_FILE _imaging.x86_64-linux-gnu.so
#zip -g $ZIP_FILE libcrypto.so.1.0.0
#zip -r -g --exclude=*.pyc* $ZIP_FILE Crypto/*
