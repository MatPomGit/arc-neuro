@echo off
setlocal
cd /d "%~dp0\..\..\.."
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set NUMEXPR_NUM_THREADS=1
set PYTHONFAULTHANDLER=1
if not exist ".venv-h1-stable-py312\Scripts\python.exe" (echo Missing .venv-h1-stable-py312 & exit /b 1)
if not exist "build\MSC-ATTACH-P01\workstation_check" mkdir "build\MSC-ATTACH-P01\workstation_check"
echo Running H1 generation-only probe...
".venv-h1-stable-py312\Scripts\python.exe" -X faulthandler manuscripts\MSC-ATTACH-P01\analysis\h1_windows_generation_probe.py > build\MSC-ATTACH-P01\workstation_check\generation_probe.log 2>&1
set CODE=%ERRORLEVEL%
type build\MSC-ATTACH-P01\workstation_check\generation_probe.log
echo.
echo Probe exit code: %CODE%
echo Log: build\MSC-ATTACH-P01\workstation_check\generation_probe.log
exit /b %CODE%
