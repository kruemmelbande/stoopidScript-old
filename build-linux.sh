rm -rf ./build
rm -rf ./dist
echo "This build only works, if your defualt python version is >=3.10, if its not, download from releases tab instead"
pyinstaller --onefile stoopidScript.py --icon=graphics/stoopidScriptLogo.ico
rm -rf ./build
mkdir build
mv ./dist/stoopidScript ./build/stoopidScript
rm -rf ./dist
echo "build done!"