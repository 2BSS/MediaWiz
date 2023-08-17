@echo off
setlocal

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