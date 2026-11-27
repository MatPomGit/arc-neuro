@echo off
setlocal
cd /d "%~dp0"
:menu
echo 1. Install dependencies
echo 2. Preliminary simulation
echo 3. Full simulation
echo 4. Custom simulation
echo 5. Exit
choice /c 12345 /n /m "Select: "
if errorlevel 5 exit /b 0
if errorlevel 4 goto custom
if errorlevel 3 goto full
if errorlevel 2 goto preliminary
python -m pip install -r requirements.txt
goto finish
:preliminary
python simulate_power.py --reps 200
goto finish
:full
echo 7 sample sizes x 4 scenarios x 5000 replications = 140000 replications
python simulate_power.py --n 40 60 80 120 160 200 300 --reps 5000
goto finish
:custom
python simulation_menu.py
:finish
if errorlevel 1 echo Operation failed.
pause
goto menu
