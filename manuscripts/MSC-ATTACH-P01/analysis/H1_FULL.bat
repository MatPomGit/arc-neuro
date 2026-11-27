@echo off
setlocal
cd /d "%~dp0\..\..\.."
echo ARC H1 FULL MONTE CARLO
echo This can take a long time. Completed chunks are resumable.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "manuscripts\MSC-ATTACH-P01\analysis\run_h1_workstation.ps1" -Mode full
if errorlevel 1 (
  echo.
  echo H1 FULL RUN FAILED OR WAS INTERRUPTED. Re-run this file to resume.
  pause
  exit /b 1
)
echo.
echo H1 FULL RUN COMPLETE.
echo Review local results. No automatic Git publication.
pause
