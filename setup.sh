#!/bin/bash

git clone https://github.com/PranovD/LLOV
cd LLOV
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python run.py
