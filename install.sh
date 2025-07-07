#!/bin/bash

echo "📦 نصب پیش‌نیازها در محیط ایزوله..."

INSTALL_DIR="/opt/sync-xui-uuid"
PYENV_DIR="$INSTALL_DIR/venv"

sudo mkdir -p $INSTALL_DIR
sudo cp -r * $INSTALL_DIR
cd $INSTALL_DIR || exit

sudo apt update -y
sudo apt install -y python3 python3-venv curl

python3 -m venv $PYENV_DIR
source $PYENV_DIR/bin/activate
pip install --no-cache-dir requests

echo "🚀 اجرای اسکریپت..."
python3 sync_xui_uuid.py
