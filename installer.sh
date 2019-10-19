#!/bin/bash

APP_HOME=$HOME/bin/remotehelper-app
APP_EXE=$HOME/bin/remotehelper
APP_ICON=$APP_HOME/icon.png

[ -d $APP_HOME ] && rm -rf $APP_HOME
[ -h $APP_EXE ] && unlink $APP_EXE

mkdir -p $APP_HOME

cp -f main.py $APP_HOME/remotehelper
chmod 755 $APP_HOME/remotehelper
cp -f icon.png $APP_ICON

ln -s $APP_HOME/remotehelper $APP_EXE

cp remotehelper.desktop $HOME/.local/share/applications/
sed -i "s~__app__~${APP_EXE}~g" "$HOME/.local/share/applications/remotehelper.desktop"
sed -i "s~__icon__~${APP_ICON}~g" "$HOME/.local/share/applications/remotehelper.desktop"