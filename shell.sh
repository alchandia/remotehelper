#!/bin/bash

# https://forums.fedoraforum.org/showthread.php?294544-gnome-terminal-title-and-ssh
# https://unix.stackexchange.com/questions/14113/is-it-possible-to-set-gnome-terminals-title-to-userhost-for-whatever-host-i

XHOSTNAME=$1
XIP=$2
XPORT=$3
XUSER=$4
XKEY=$5

# Changes the PS1 and title
SETTP='MY_PROMPT="$XUSER@$XHOSTNAME\$ "'
SETTP="$SETTP;"'MY_TITLE="\[\e]0;$XUSER@$XHOSTNAME\a\]"'
SETTP="$SETTP;"'PS1="$MY_TITLE$MY_PROMPT"'

# The actual ssh connection
/usr/bin/ssh -A -i $XKEY -t $XUSER@$XIP:$XPORT "export XUSER=$XUSER; export XHOSTNAME=$XHOSTNAME; export PROMPT_COMMAND='eval '\\''$SETTP'\\'; bash --login"