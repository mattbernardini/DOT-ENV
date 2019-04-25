#!/bin/bash
ln -s -f $PWD/vimrc $HOME/.vimrc
ln -s -f $PWD/bashrc $HOME/.bashrc
ln -s -f $PWD/gdbinit $HOME/.gdbinit
ln -s -f $PWD/bash_logout $HOME/.bash_logout
ln -s -f $(which bash) $HOME/bin/sh
ln -s -f $(which aclocal) $HOME/bin/aclocal-1.14
ln -s -f $(which automake) $HOME/bin/automake-1.14

