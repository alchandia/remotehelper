#!/bin/bash

APP_HOME=$HOME/bin/remotehelper-app
APP_EXE=$HOME/bin/remotehelper

[ -d $APP_HOME ] && rm -rf $APP_HOME
[ -h $APP_EXE ] && unlink $APP_EXE

mkdir -p $APP_HOME

cp -f main.py $APP_HOME/remotehelper
chmod 755 $APP_HOME/remotehelper
cp -f icon.png $APP_HOME/
cp -f ssh_connection.sh $APP_HOME/

ln -s $APP_HOME/remotehelper $APP_EXE