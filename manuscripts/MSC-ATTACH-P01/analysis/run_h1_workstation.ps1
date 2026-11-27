param(
    [ValidateSet("check","full")]
    [string]$Mode = "check",
    [int]$Workers = 0
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
Set-Location $RepoRoot
$Python = ".\.venv-h1-stable-py312\Scripts\python.exe"

# Keep native BLAS/OpenMP libraries single-threaded inside each Python process.
# The Monte Carlo parallelism is managed at the process/chunk level.
$env:OPENBLAS_NUM_THREADS = "1"
$env:OMP_NUM_THREADS = "1"
$env:MKL_NUM_THREADS = "1"
$env:NUMEXPR_NUM_THREADS = "1"
$env:VECLIB_MAXIMUM_THREADS = "1"

Write-Host "=== ARC H1 workstation pipeline ==="
Write-Host "Mode: $Mode"

if (-not (Test-Path $Python)) {
    $created = $false
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.12 -m venv .venv-h1-stable-py312
        $created = ($LASTEXITCODE -eq 0)
    }
    if (-not $created -and (Get-Command python -ErrorAction SilentlyContinue)) {
        python -m venv .venv-h1-stable-py312
        $created = ($LASTEXITCODE -eq 0)
    }
    if (-not $created) {
        throw "Python 3.12 is required for the H1 Windows Monte Carlo environment."
    }
}
$Version = (& $Python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')").Trim()
if ($Version -ne "3.12") {
    throw "H1 Windows Monte Carlo requires Python 3.12; resolved interpreter reports $Version."
}
Write-Host "H1 interpreter: Python $Version"
& $Python -m pip install --disable-pip-version-check -r manuscripts/MSC-ATTACH-P01/analysis/requirements-lock.txt
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }

& $Python manuscripts/MSC-ATTACH-P01/analysis/run_h1_tests_isolated.py
if ($LASTEXITCODE -ne 0) { throw "Isolated unit tests failed. Simulation was not started." }

if ($Mode -eq "check") {
    foreach ($n in @(72,84)) {
        foreach ($truth in @("M0","M1","M2","M3","M4")) {
            Write-Host "Development check: N=$n, truth=$truth, 20 replications in isolated single-replication processes, compliance=.75, missingness=1"
            for ($start = 0; $start -lt 20; $start += 1) {
                $out = "build\MSC-ATTACH-P01\workstation_check\n$n\$truth\r$start"
                New-Item -ItemType Directory -Force -Path $out | Out-Null
                $log = Join-Path $out "run.log"
                $cmd = "`"$Python`" manuscripts/MSC-ATTACH-P01/analysis/h1_exact_monte_carlo.py --config manuscripts/MSC-ATTACH-P01/protocol/exact_design_config.json --output-dir `"$out`" --rep-start $start --replications 1 --couples $n --compliance 0.75 --missingness 1 --truth $truth"
                cmd /d /s /c "$cmd > `"$log`" 2>&1"
                $code = $LASTEXITCODE
                if (Test-Path $log) { Get-Content $log | Write-Host }
                if ($code -ne 0) {
                    throw "Development check failed for N=$n, truth=$truth, start=$start, exit=$code. Full diagnostic log: $log"
                }
            }
        }
    }
    Write-Host "CHECK COMPLETE. Next command:"
    Write-Host ".\manuscripts\MSC-ATTACH-P01\analysis\run_h1_workstation.ps1 -Mode full"
    exit 0
}

$runnerArgs = @("-ExecutionPolicy","Bypass","-File","manuscripts/MSC-ATTACH-P01/analysis/run_h1_full_windows.ps1","-Python",$Python)
if ($Workers -gt 0) { $runnerArgs += @("-Workers",$Workers) }
& powershell @runnerArgs
if ($LASTEXITCODE -ne 0) { throw "Full Monte Carlo pipeline failed." }

$results = "build\MSC-ATTACH-P01\exact_results"
$manifest = Join-Path $results "merged\h1_exact_merge_manifest.json"
$decision = Join-Path $results "decisions\h1_decision_matrix.csv"
if (-not (Test-Path $manifest)) { throw "Missing merge manifest after full run." }
if (-not (Test-Path $decision)) { throw "Missing decision matrix after full run." }

$meta = [ordered]@{
    completed_at_local = (Get-Date).ToString("o")
    computer = $env:COMPUTERNAME
    logical_processors = [Environment]::ProcessorCount
    workers_requested = $Workers
    python = (& $Python --version 2>&1 | Out-String).Trim()
    git_commit = (git rev-parse HEAD).Trim()
    gpu_note = "GPU is not used by the current statsmodels GEE simulation."
}
$meta | ConvertTo-Json | Set-Content (Join-Path $results "workstation_run_metadata.json") -Encoding UTF8

Write-Host "FULL RUN COMPLETE AND VERIFIED."
Write-Host "Review local results. Do not commit raw outputs or workstation metadata."
Write-Host "Raw chunks remain local and are ignored by Git."
