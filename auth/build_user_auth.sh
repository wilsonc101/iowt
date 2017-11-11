#!/bin/bash

ENV_LIBS="/home/chris/.virtualenvs/iowt-auth/lib/python2.7/site-packages"
APP="/home/chris/dev/iowt/auth/iowt-user-auth"
ZIP_FILE="/home/chris/iowt-user-auth.zip"



rm $ZIP_FILE

zip -9 $ZIP_FILE

cd $ENV_LIBS
zip -9 -r --exclude=*.pyc* $ZIP_FILE .



cd $APP
zip -g $ZIP_FILE app.py
zip -g $ZIP_FILE libssl.so.1.0.0
zip -g $ZIP_FILE libcrypto.so.1.0.0
zip -r -g --exclude=*.pyc* $ZIP_FILE Crypto/*
