@echo off
setlocal
cd /d "%~dp0\..\..\.."

set PYTHON=.\.venv-h1-stable-py312\Scripts\python.exe
set CONFIG=manuscripts\MSC-ATTACH-P01\protocol\h1_asymmetry_validation_config.json
set OUT=build\MSC-ATTACH-P01\asymmetry_validation

echo ARC H1 FOCUSED M4 ASYMMETRY VALIDATION
echo.
echo Design:
echo   N = 84 couples
echo   compliance = 0.75, 0.85
echo   missingness strength = 0, 1
echo   truths = M3, M4
echo   replications = 1000 per cell
echo   total = 8000 replications
echo.
echo Historical N=84 design only; final recruitment N is not locked.
echo Development sensitivity analysis; no confirmatory tolerance is established.
echo.

if not exist "%PYTHON%" (
  echo Missing stable H1 Python environment: %PYTHON%
  echo Run H1_CHECK.bat first to create/verify the environment.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File manuscripts\MSC-ATTACH-P01\analysis\run_h1_full_windows.ps1 ^
  -ConfigPath "%CONFIG%" ^
  -OutputRoot "%OUT%" ^
  -Replications 1000 ^
  -ChunkSize 10 ^
  -SkipPostMergeAnalyses

if errorlevel 1 (
  echo.
  echo FOCUSED ASYMMETRY MONTE CARLO FAILED.
  pause
  exit /b 1
)

"%PYTHON%" manuscripts\MSC-ATTACH-P01\analysis\h1_asymmetry_operating_characteristics.py ^
  --input "%OUT%\merged\h1_exact_replications.csv" ^
  --config "%CONFIG%" ^
  --output-dir "%OUT%\asymmetry"

if errorlevel 1 (
  echo.
  echo ASYMMETRY OPERATING-CHARACTERISTIC ANALYSIS FAILED.
  pause
  exit /b 1
)

echo.
echo H1 ASYMMETRY VALIDATION COMPLETE.
echo Review:
echo   %OUT%\asymmetry\h1_asymmetry_candidate_guardrails.csv
echo   %OUT%\asymmetry\h1_asymmetry_operating_characteristics.csv
echo.
echo Do not lock delta_asym solely from a favorable simulation cell.
pause
