@echo off

:: Check if the virtual environment is already activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call VenvSetup.bat
)

cd verifier
python main.py
cd ..