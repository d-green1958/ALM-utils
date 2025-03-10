# ALM-utils
Contains:
- a python package named pyALMTree which is collection of useful functions to be used with ALM for openFOAM v2006. 
- openFoam function objects to be used in conjuction with ALM such as phase averaging.

<div style="text-align: center;">
<img src="logo/pyALMTree-logo.png" alt="drawing" style="width:200px;"/>
</div>

## Installation
Enter the following into your terminal:
```
git clone https://github.com/d-green1958/ALM-utils.git
```
Now run the install script
```
./install.sh
```
That's it!

## Manual Installation
Install PyhD (a submodule)
```
cd PhD-Formatting
cd PyhD
pip install .
cd ../..
```
>[!NOTE]
>You may want to fork your own PyhD package for customisation

To install the pyALMTree
```
cd python
pip install .
cd ..
```
or alternativly with the editable flag
```
cd python
pip install -e .
cd ..
```
Now that the python package has been installed, source the bashrc file in your bashrc
```
echo "source $(pwd)/bashrc" >> ~/.bashrc 
```
