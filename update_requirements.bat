call .\venv\Scripts\activate.bat

call pip freeze | findstr /V /C:"condingtime" > requirements.txt