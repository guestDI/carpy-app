#!/bin/bash

if [ ! -d "venv" ]; then
  echo "New virtual environment..."
  python3 -m venv venv
fi

echo "Activating..."
source venv/bin/activate

if [ -f "requirements.txt" ]; then
  echo "Installing deps..."
  pip install -r requirements.txt
else
  echo "File requirements.txt is not found!"
fi
