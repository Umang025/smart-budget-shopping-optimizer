@echo off
title Smart Budget and Shopping Optimizer
echo =====================================================================
echo  Smart Budget and Shopping Optimizer - DAA MCA Mini Project
echo =====================================================================
echo.

where python >nul 2>nul
if %errorlevel% equ 0 (
    python main.py
    goto end
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    py main.py
    goto end
)

if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" (
    "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" main.py
    goto end
)

echo [ERROR] Python not found in PATH or standard runtime paths.
echo Please install Python 3.10+ and add it to PATH.
pause

:end
