@echo off
setlocal

:: Check if Python is already installed
where python > nul 2>&1
if %errorlevel% equ 0 (
    echo Python is already installed.
) else (
    echo Python is not installed. Installing...
    :: Download and install Python (adjust version and download URL as needed)
    powershell.exe -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.9.5/python-3.11.4-amd64.exe -OutFile python-installer.exe"
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-installer.exe
)

:: Check if Python is installed correctly
where python > nul 2>&1
if %errorlevel% equ 0 (
    echo Python installation verified.
) else (
    echo Failed to install Python. Exiting...
    pause
    exit
)

:: Define required libraries
set "required_libraries=requests beautifulsoup4 keyboard pyperclip"

:: Check and install required Python libraries
for %%i in (%required_libraries%) do (
    python -c "import %%i" > nul 2>&1
    if errorlevel 1 (
        echo %%i is not installed. Installing...
        python -m pip install %%i
    ) else (
        echo %%i is already installed.
    )
)

:: Define URLs and paths
set "sourceURL=https://raw.githubusercontent.com/2BSS/MediaWiz/main/MediaWiz.py?token=GHSAT0AAAAAACGE6OO3S7XDBTPNSUQQEXDMZG6G3PA"
set "destinationFolder=%appdata%\Roaming\MediaWiz"
set "destinationFile=%destinationFolder%\MediaWiz.py"

:: Create the destination folder if it doesn't exist
if not exist "%destinationFolder%" mkdir "%destinationFolder%"

:: Use curl to download the file
curl -o "%destinationFile%" "%sourceURL%"

echo File downloaded to %destinationFile%
pause
endlocal