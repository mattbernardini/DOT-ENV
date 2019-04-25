#!/bin/bash
# 3.1 Introduction
# -v is Verbose 
# -p is create parents if needed
# a+wt makes directory sticky so only owner of a file can delete
(mkdir -v -p $LFS/sources && chmod -v a+wt $LFS/sources)
wget http://www.linuxfromscratch.org/lfs/view/stable/wget-list > wget-list.txt
wget --input-file=wget-list.txt --continue --directory-prefix=$LFS/sources
(cd $LFS/sources && git clone https://github.com/openssl/openssl.git && cd openssl && ./config --prefix=$HOME && make && make test && make install)
(cd $LFS/sources && git clone https://github.com/git/git && cd git && make configure && ./configure --prefix=$HOME && make install)
git clone https://github.com/jwilk-mirrors/texinfo.git
(mkdir -v -p $LFS/tools && chmod -v a+wt $LFS/tools)
