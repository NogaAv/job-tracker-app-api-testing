@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PYTHON_BIN=%PYTHON_BIN%"

if not defined PYTHON_BIN (
    if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
        set "PYTHON_BIN=%SCRIPT_DIR%.venv\Scripts\python.exe"
    ) else (
        where py >nul 2>nul
        if not errorlevel 1 (
            set "PYTHON_BIN=py -3"
        ) else (
            set "PYTHON_BIN=python"
        )
    )
)

if "%PYTHON_BIN%"=="py -3" (
    py -3 "%SCRIPT_DIR%run_tests.py" %*
) else (
    "%PYTHON_BIN%" "%SCRIPT_DIR%run_tests.py" %*
)
