#!/bin/bash

echo "Starting Termux AI assistant setup..."

# Update Termux packages
pkg update -y
pkg upgrade -y

# Install Python and Termux API if not installed
pkg install -y python git termux-api

# Make sure pip is installed (do NOT upgrade it!)
# Termux already ships with pip
pip install --no-cache-dir pyautogui keyboard

# Grant storage permission
termux-setup-storage

echo "✅ Termux setup complete! You can now run the AI assistant."
echo "Run: python main.py"
