#!/usr/bin/env bash

mv ~/.vim ~/.vim.orig
mv ~/.vimrc ~/.vimrc.orig

cp -rf .vim ~
cp -rf .vimrc ~

vim +PluginInstall +qall
