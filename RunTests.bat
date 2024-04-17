@echo off

:: Check if the virtual environment is already activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call VenvSetup.bat
)

cd tests
call pytest test_json_data_verifier.py
cd ..
