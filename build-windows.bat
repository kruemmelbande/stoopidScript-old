@echo off
rmdir /q /s .\build
rmdir /q /s .\dist
echo This build only works, if your defualt python version is >=3.10, if its not, download from releases tab instead
pyinstaller --onefile stoopidScript.py --icon=graphics/stoopidScriptLogo.ico
rmdir /q /s .\build
mkdir build
move .\dist\stoopidScript.exe .\build\stoopidScript.exe
rmdir /q /s .\dist
del stoopidScript.spec
echo build done!