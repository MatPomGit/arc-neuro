@echo off
setlocal
cd /d "%~dp0\..\..\.."
echo ARC H1 COMPARABLE-LAG RECALIBRATION
echo Focused grid: N=72/84/96/108/120, compliance=.75, missingness=0/1.
echo Results are resumable and do not overwrite historical exact_results.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "manuscripts\MSC-ATTACH-P01\analysis\run_h1_recalibration_windows.ps1"
if errorlevel 1 (
  echo.
  echo H1 RECALIBRATION FAILED OR WAS INTERRUPTED. Re-run to resume.
  pause
  exit /b 1
)
echo.
echo H1 RECALIBRATION COMPLETE.
pause
