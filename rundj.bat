@echo off
setlocal

REM Activate the virtual environment.
call venv\Scripts\activate

REM Navigate to your Django project directory.
cd cuisine

REM Start the Django development server in the background.
start /B py manage.py runserver 0.0.0.0:8000

REM Wait for a moment to ensure the server starts (adjust the delay if needed).
timeout /t 5 /nobreak

REM Open the website link in your default web browser.
start http://192.168.1.13:8000

REM Deactivate the virtual environment when you're done.
call venv\Scripts\deactivate

endlocal
