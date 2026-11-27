@echo off
setlocal
cd /d "%~dp0\..\..\.."
echo ARC H1 workstation check
powershell -NoProfile -ExecutionPolicy Bypass -File "manuscripts\MSC-ATTACH-P01\analysis\run_h1_workstation.ps1" -Mode check
if errorlevel 1 (
  echo.
  echo H1 CHECK FAILED.
  pause
  exit /b 1
)
echo.
echo H1 CHECK COMPLETE.
pause
