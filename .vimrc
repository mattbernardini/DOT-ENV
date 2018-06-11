set nocompatible		" be iMproved, required
filetype off			" required
"To have numbers on the side
set number
let g:ycm_server_python_interpreter = '/usr/bin/python'
let g:ycm_show_diagnostics = 0
" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim

call vundle#begin()
" Plugins
Plugin 'VundleVim/Vundle.vim'
Plugin 'Valloric/YouCompleteMe'
Plugin 'scrooloose/nerdtree'
Plugin 'bling/vim-airline'
Plugin 'rdnetto/YCM-Generator'
Plugin 'tpope/vim-fugitive'
Plugin 'scrooloose/syntastic'
Plugin 'horosphere/formatgen'
call vundle#end()
filetype plugin indent on
set expandtab
set tabstop=2
set softtabstop=2
set shiftwidth=2
syntax enable
"Auto start NERDTree by default
autocmd vimenter * NERDTree
"set tabstop=4 softtabstop=4 expandtab shiftwidth=4 smarttab


