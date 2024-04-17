@echo off

python -m venv .venv

:: Activate virtual environment
call .venv\Scripts\activate

:: install pytest
pip install pytest