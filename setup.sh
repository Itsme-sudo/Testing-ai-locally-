#!/bin/bash
echo "Detecting OS..."
OS=$(uname | tr '[:upper:]' '[:lower:]')

if [ -e "/data/data/com.termux/files/home" ]; then
    echo "Setting up Termux..."
    pkg update -y
    pkg install -y python git termux-api
    pip install --upgrade pip
    pip install pyautogui keyboard
    termux-setup-storage
    echo "Termux setup complete!"
elif [[ "$OS" == "linux" ]]; then
    echo "Setting up Linux..."
    sudo apt update
    sudo apt install -y python3-pip xdotool
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    echo "Linux setup complete!"
elif [[ "$OS" == "darwin" ]]; then
    echo "Setting up macOS..."
    brew install python
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
    echo "macOS setup complete!"
elif [[ "$OS" == "windows" || "$OS" == "mingw64" ]]; then
    echo "Setting up Windows..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo "Windows setup complete!"
else
    echo "Unknown OS: $OS"
fi
