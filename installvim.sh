#!/bin/bash

# install dependencies
sudo apt-get install libncurses5-dev python-dev libperl-dev ruby-dev liblua5.2-dev python3-dev

# Fix liblua paths
sudo ln -s /usr/include/lua5.2 /usr/include/lua
sudo ln -s /usr/lib/x86_64-linux-gnu/liblua5.2.so /usr/local/lib/liblua.so

# Clone vim sources
cd ~/build
git clone https://github.com/vim/vim.git

cd vim
./configure --prefix=$HOME    \
    --enable-luainterp=yes    \
    --enable-perlinterp=yes   \
    --enable-pythoninterp=yes \
    --enable-python3interp=yes\
    --enable-rubyinterp=yes   \
    --enable-cscope           \
    --disable-netbeans        \
    --enable-multibyte        \
    --enable-largefile        \
    --enable-gui=no           \
    --with-features=huge      \

make -j12 && make install

cd ~/build
tar -xzvf ctags-5.8.tar.gz
cd ctags-5.8
./configure --prefix=$HOME
make && make install
