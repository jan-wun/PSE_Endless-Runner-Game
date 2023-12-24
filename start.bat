@echo off

REM Create virtual environment.
python -m venv venv

set original_dir=%CD%
set venv_root_dir="venv"

cd %venv_root_dir%

REM Activate virtual environment.
call Scripts\activate.bat

pip install -r "%original_dir%\requirements.txt"

call Scripts\deactivate.bat
REM Deactivate virtual environment.

cd %original_dir%

REM Start the endless runner game.
call venv\Scripts\python.exe main.py