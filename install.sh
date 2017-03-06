#!/usr/bin/env bash

mv ~/.vim ~/.vim.orig
mv ~/.vimrc ~/.vimrc.orig

cp -rf .vim ~
cp -rf .vimrc ~

echo "alias vi=vim" >> ~/.bashrc
source ~/.bashrc
#vim +PluginInstall +qall
