REM Calls the python script that does the wallpaper change
REM This checks that python is installed and if not, how to install

@echo off

py --version

IF %errorlevel% neq 0 goto pyError
    echo We need to pick somewhere to put the wallpapers. Default is 
    set /p pic_folder=
    py wallpaper.py
    pause
    exit /b 0
    
    
    
:pyError
    echo Py not installed, checking for Python3
    python3 --version
    IF %errorlevel% neq 0 goto pythonError
        
:pythonError
echo Python3 not installed.
echo This script needs python 3.7+ installed to work.
echo Either it is not installed or it's not in your path.
echo Please install Python3 from https://www.python.org/downloads/windows/ or
echo add your installed Python3.x to your path: https://geek-university.com/python/add-python-to-the-windows-path/
pause
exit /b 1
