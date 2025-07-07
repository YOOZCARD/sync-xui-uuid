#!/bin/bash

INSTALL_DIR="/opt/sync-xui-uuid"
PYENV_DIR="$INSTALL_DIR/venv"

echo "📦 نصب پیش‌نیازها در محیط ایزوله..."
sudo mkdir -p $INSTALL_DIR
sudo cp -r $(dirname "$0")/* $INSTALL_DIR
cd $INSTALL_DIR || exit

sudo apt update -y
sudo apt install -y python3 python3-venv curl

python3 -m venv $PYENV_DIR
source $PYENV_DIR/bin/activate
pip install --no-cache-dir requests

echo "🚀 اجرای اسکریپت..."
$PYENV_DIR/bin/python3 $INSTALL_DIR/sync_xui_uuid.py
