#!/bin/bash
cd PhD-Formatting
cd PyhD
pip install .
cd ../..
cd python
pip install -e .
cd ..
echo "source $(pwd)/bashrc" >> ~/.bashrc 
