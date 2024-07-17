#!/bin/bash

exec_str="uv venv "

# 获得当前目录当做项目名, 用于创建虚拟环境，在 exec_str 后面加上 ". + 项目名"
project_name=$(basename "$(pwd)")
exec_str+=".$project_name"

# 如果.env中有指定 python 目录，则使用指定的 python 目录 -p
if [ -f .env ] && grep -q "^PYTHON_PATH=" .env; then
    python_path=$(grep "^PYTHON_PATH=" .env | cut -d '=' -f2)
    exec_str+=" -p $python_path"
fi

# 执行命令
eval $exec_str

source ".$project_name/bin/activate"

# 安装依赖
uv pip install -r uv.poetry.txt

echo "source .$project_name/bin/activate" >> .env
echo "PATH=$(pwd)/.py-template/bin:\$PATH" >> .env

# 获取 Git 用户信息
GIT_NAME=$(git config user.name)
GIT_EMAIL=$(git config user.email)

# 获取当前目录名
DIR_NAME=$(basename "$PWD")

# 更新 pyproject.toml
sed -i "s/authors = .*/authors = [\"$GIT_NAME <$GIT_EMAIL>\"]/" pyproject.toml
sed -i "s/name = .*/name = \"$DIR_NAME\"/" pyproject.toml