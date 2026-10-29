@echo off
cd /d "%~dp0"
title MINSS Android Engine V5.1 Debug
where py >nul 2>nul
if not errorlevel 1 (
  py -3 minss.py
  if not errorlevel 1 goto end
)
where python >nul 2>nul
if not errorlevel 1 (
  python minss.py
  if not errorlevel 1 goto end
)
echo.
echo MINSS could not start. Python 3 may not be installed or may not be on PATH.
echo Install Python from https://www.python.org/downloads/windows/ and enable Add python.exe to PATH.
echo If a startup error file exists, open minss_startup_error.txt in this folder.
pause
:end
