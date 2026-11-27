@echo off
setlocal
cd /d "%~dp0..\..\.."
set "ANALYSIS=manuscripts\MSC-ATTACH-P02\analysis"
set "OUT=build\MSC-ATTACH-P02\experiments"
set "VENV=build\MSC-ATTACH-P02\venv"
set "PY=%VENV%\Scripts\python.exe"
if not exist "%PY%" (
  python -m venv "%VENV%"
  if errorlevel 1 exit /b 1
)
"%PY%" -m pip install -r "%ANALYSIS%\requirements-lock.txt"
if errorlevel 1 exit /b 1
set "MPLBACKEND=Agg"
"%PY%" -B "%ANALYSIS%\run.py" --csv "%OUT%\trajectory.csv"
if errorlevel 1 exit /b 1
"%PY%" -B "%ANALYSIS%\fit_controller.py" "%OUT%\trajectory.csv" --output "%OUT%\controller_fit.json"
if errorlevel 1 exit /b 1
"%PY%" -B "%ANALYSIS%\reproduce.py" --output "%OUT%"
if errorlevel 1 exit /b 1
echo Synthetic development experiments complete: %OUT%
exit /b 0
