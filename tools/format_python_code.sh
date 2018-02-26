#!/bin/bash

# 用来格式化代码，提交前使用，保证大家格式一样，好看~
base_dir=$(dirname "$(cd "$(dirname "$0")" || return; pwd)")

echo "$base_dir"

while true; do
    read -rp "确认代码没有语法问题吗？" yn
    case $yn in
        [Yy]* ) yapf -ir "$base_dir" -e migrations; isort -rc --atomic "$base_dir"; yapf -ir "$base_dir" -e migrations; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
