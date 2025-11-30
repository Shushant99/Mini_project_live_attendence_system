@echo off
REM ---------- Configuration ----------
REM Project folder (where manage.py lives)
set "PROJECT_DIR=D:\codes\python\Mini_project_live_attendence_system"

REM Name of the conda env (if you used conda); change if different
set "CONDA_ENV=attend-env"

REM Relative path to venv activate script (if you used python -m venv)
set "VENV_ACTIVATE=%PROJECT_DIR%\.venv\Scripts\activate.bat"
REM also check .\venv\Scripts\activate.bat
set "VENV_ACTIVATE2=%PROJECT_DIR%\venv\Scripts\activate.bat"

REM ---------- Script starts ----------
echo Starting Smart Attendance runner...
echo.

REM Try to activate conda env (preferred). This uses the conda 'activate' batch wrapper.
where conda >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found conda. Activating conda environment "%CONDA_ENV%"...
    REM Activate conda base scripts first, then activate the env
    CALL C:\Users\susha\miniconda3\Scripts\activate.bat" 2>nul
    REM if miniconda installed elsewhere, above may fail; try generic 'conda activate'
    conda activate %CONDA_ENV% 2>nul
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to activate conda env %CONDA_ENV%. Trying to continue...
    )
) else (
    echo conda not found in PATH.
)

REM If conda not active, try venv activation (project local)
if "%CONDA_PREFIX%"=="" (
    if exist "%VENV_ACTIVATE%" (
        echo Activating venv at %VENV_ACTIVATE%...
        CALL "%VENV_ACTIVATE%"
    ) else if exist "%VENV_ACTIVATE2%" (
        echo Activating venv at %VENV_ACTIVATE2%...
        CALL "%VENV_ACTIVATE2%"
    ) else (
        echo No venv found at %VENV_ACTIVATE% or %VENV_ACTIVATE2%. Ensure your env is activated manually.
    )
) else (
    echo Conda env active: %CONDA_PREFIX%
)

REM Switch to project drive and directory
pushd "%PROJECT_DIR%" || (
    echo Failed to change dir to %PROJECT_DIR%
    pause
    exit /b 1
)

REM OPTIONAL: run migrations automatically (comment out if you don't want)
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

REM OPTIONAL: run encoding generation script automatically (uncomment if you want)
REM echo Generating face encodings...
REM python scripts/generate_encodings.py

REM Start server
echo Starting Django dev server...
python manage.py runserver 0.0.0.0:8000

REM Keep window open after server stops
pause
