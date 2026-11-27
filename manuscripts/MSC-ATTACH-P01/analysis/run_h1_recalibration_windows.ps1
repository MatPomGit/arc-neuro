param(
    [int]$Workers = 0,
    [int]$Replications = 1000,
    [int]$ChunkSize = 10,
    [string]$Python = ".\.venv-h1-stable-py312\Scripts\python.exe",
    [string]$OutputRoot = "build\MSC-ATTACH-P01\comparable_lag_recalibration"
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
Set-Location $RepoRoot

$Config = "manuscripts\MSC-ATTACH-P01\protocol\h1_comparable_lag_recalibration_config.json"
$Output = $OutputRoot

if (-not (Test-Path $Python)) {
    if ($Python -ne ".\.venv-h1-stable-py312\Scripts\python.exe") {
        throw "Explicit Python path not found: $Python"
    }
    $created = $false
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.12 -m venv .venv-h1-stable-py312
        $created = ($LASTEXITCODE -eq 0)
    }
    if (-not $created -and (Get-Command python -ErrorAction SilentlyContinue)) {
        python -m venv .venv-h1-stable-py312
        $created = ($LASTEXITCODE -eq 0)
    }
    if (-not $created) { throw "Python 3.12 is required." }
}
$Version = (& $Python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')").Trim()
if ($Version -ne "3.12") { throw "H1 recalibration requires Python 3.12; got $Version." }
& $Python -m pip install --disable-pip-version-check -r manuscripts/MSC-ATTACH-P01/analysis/requirements-lock.txt
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }
& $Python -m unittest discover -s manuscripts/MSC-ATTACH-P01/analysis -p "test_h1*.py"
if ($LASTEXITCODE -ne 0) { throw "H1 unit tests failed; recalibration not started." }

$args = @(
    "-ExecutionPolicy","Bypass",
    "-File","manuscripts\MSC-ATTACH-P01\analysis\run_h1_full_windows.ps1",
    "-Python",$Python,
    "-ConfigPath",$Config,
    "-OutputRoot",$Output,
    "-Replications",$Replications,
    "-ChunkSize",$ChunkSize
)
if ($Workers -gt 0) { $args += @("-Workers",$Workers) }

& powershell @args
if ($LASTEXITCODE -ne 0) { throw "Comparable-lag recalibration simulation failed." }

$primary = Join-Path $Output "inference\h1_primary_operating_characteristics.csv"
if (-not (Test-Path $primary)) { throw "Missing revised inference operating characteristics: $primary" }

& $Python manuscripts/MSC-ATTACH-P01/analysis/h1_recalibration_summary.py --primary-oc $primary --config $Config --output-dir (Join-Path $Output "recalibration")
if ($LASTEXITCODE -ne 0) { throw "Recalibration decision summary failed." }

Write-Host ""
Write-Host "H1 COMPARABLE-LAG RECALIBRATION COMPLETE"
Write-Host "Review:"
Write-Host "  $Output\recalibration\h1_recalibration_report.md"
Write-Host "  $Output\recalibration\h1_recalibration_decision.json"
