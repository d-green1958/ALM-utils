#!/bin/bash
cd PhD-Formatting
cd PyhD
pip install -e .
cd ../..
cd pyALMTree
pip install -e .
cd ..
echo "source $(pwd)/bashrc" >> ~/.bashrc 
