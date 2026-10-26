@echo off
chcp 65001 >nul
setlocal
if not exist "%~dp0Booth-design-private-pilot\START_BOOTHFORGE_WINDOWS.cmd" (
    echo Extract the entire ZIP into a new folder first.
    pause
    exit /b 1
)
call "%~dp0Booth-design-private-pilot\START_BOOTHFORGE_WINDOWS.cmd"
endlocal
