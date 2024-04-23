@echo off
setlocal

rem setting variables
rem Get the path to the user's profile directory
set "profilePath=%USERPROFILE%"

rem Construct the full paths to the source file and the desktop
rem set "sourceFile=%profilePath%\Path\To\Your\File.ext"
set "desktopPath=%profilePath%\OneDrive\Desktop"

rem Run cmd
cd %~dp0..\taskpoint\program
set "sourcePath=%CD%\TaskPoint.exe"

rem Run pyInstaller
pyinstaller "main.py" --onefile --window

rem Move main.py created into the main folder of the project
move dist\main.exe

rem Delete the dist file that is unused
rmdir /s /q dist

rem Create a shortcut to the source file on the desktop
mklink "D:\TaskPoint.lnk" "%sourcePath%"

endlocal

rem Check if the desktop path contains the OneDrive path
rem echo %desktopPath% | find /i "%oneDrivePath%" > nul

if %errorlevel% neq 0 (
    echo An error occurred!
    pause
)