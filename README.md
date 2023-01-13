# ABD Command Util

[![Generic badge](https://img.shields.io/badge/Python-v3.11-blue.svg)](https://shields.io/)


This little program is going to simplify the original adb command and based on [`adb-shell`](https://github.com/JeffLIrion/adb_shell) to develop the following command.

- `\c` to connect the first usb of Android device 
- `\> {folder name}` go forward to a specific folder
    - E.g `\> storage`
- `\<` fo backward
- `\l` listing the current folder
- `\la` listing the current folder in details
- `\get {file name}` download a specific file from device to local current directory
    - E.g `\get README.MD`
- `\up {file path}` upload a specific local file to currect device directory
    - E.g `\up app.py`
- `\del {file name}` delete a specific file from the current device directory
    - E.g `\del README.MD`
- `\q` quit the program

## Start this program
1. Install Python version up to v3.11
2. Clone all the source files
3. Prepare a virtual env
4. Install required libray by using requirements.txt
5. Run up the app.py with sudo `sudo python app.py` 
    - for accessing USB permission especially in MacOs