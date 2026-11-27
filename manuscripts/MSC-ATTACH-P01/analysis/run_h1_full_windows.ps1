param(
    [int]$Workers = 0,
    [int]$ChunkSize = 10,
    [int]$Replications = 1000,
    [int]$MaxAttempts = 3,
    [string]$Python = ".\.venv-h1-stable-py312\Scripts\python.exe",
    [string]$OutputRoot = "build\MSC-ATTACH-P01\exact_results",
    [string]$ConfigPath = "manuscripts\MSC-ATTACH-P01\protocol\exact_design_config.json",
    [switch]$SkipPostMergeAnalyses
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
Set-Location $RepoRoot
$AllowedRoot = [IO.Path]::GetFullPath((Join-Path $RepoRoot "build\MSC-ATTACH-P01")) + [IO.Path]::DirectorySeparatorChar
$OutputRoot = [IO.Path]::GetFullPath($OutputRoot)
if (-not $OutputRoot.StartsWith($AllowedRoot, [StringComparison]::OrdinalIgnoreCase)) { throw "OutputRoot must be under build/MSC-ATTACH-P01." }
# Bind resumable chunks to the exact configuration, code revision and replication count.
$Identity = [ordered]@{ config_sha256 = (Get-FileHash -Algorithm SHA256 $ConfigPath).Hash; revision = (git rev-parse HEAD).Trim(); replications = $Replications; chunk_size = $ChunkSize }
if ($LASTEXITCODE -ne 0) { throw "Cannot identify Git revision." }
$IdentityJson = $Identity | ConvertTo-Json -Compress
$IdentityFile = Join-Path $OutputRoot "run_identity.json"
if (Test-Path $OutputRoot) {
 if (-not (Test-Path $IdentityFile) -or (Get-Content $IdentityFile -Raw).Trim() -ne $IdentityJson) { throw "Existing output has no matching run identity; choose a fresh OutputRoot." }
} else {
 New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null
 $IdentityJson | Set-Content -Path $IdentityFile -Encoding UTF8
}
if ($Workers -le 0) {
    $logical = [Environment]::ProcessorCount
    # Conservative default for Windows stability: never exceed four
    # concurrent Python processes and use at most 25% of logical CPUs.
    $cpuTarget = [Math]::Max(1, [Math]::Floor($logical * 0.25))
    try {
        $os = Get-CimInstance Win32_OperatingSystem
        $freeGiB = [double]$os.FreePhysicalMemory / 1MB
        $memoryTarget = [Math]::Max(1, [Math]::Floor($freeGiB / 2.5))
        $Workers = [Math]::Max(1, [Math]::Min(4, [Math]::Min($cpuTarget, $memoryTarget)))
    } catch {
        $Workers = [Math]::Max(1, [Math]::Min(4, $cpuTarget))
    }
}
if ($ChunkSize -le 0 -or $Replications -le 0 -or $MaxAttempts -le 0) { throw "ChunkSize, Replications, and MaxAttempts must be positive." }
if (-not (Test-Path $Python)) { throw "Python not found: $Python. Create .venv-h1-stable-py312 first." }

$configPath = $ConfigPath
if (-not (Test-Path $configPath)) { throw "Config not found: $configPath" }
$config = Get-Content $configPath -Raw | ConvertFrom-Json

function Test-H1ChunkComplete {
 param(
  [string]$Out,
  [int]$Start,
  [int]$Count
 )

 $completeMarker = Join-Path $Out "_COMPLETE"
 if (-not (Test-Path $completeMarker)) { return $false }

 $expected = @($Start..($Start + $Count - 1))
 $batchCsv = Join-Path $Out "h1_exact_replications.csv"
 if ((Test-Path $batchCsv) -and ((Get-Item $batchCsv).Length -gt 0)) {
  try {
   $rows = @(Import-Csv $batchCsv)
   if ($rows.Count -eq $Count) {
    $actual = @($rows | ForEach-Object { [int]$_.replication } | Sort-Object)
    if ((Compare-Object $expected $actual).Count -eq 0) {
     return $true
    }
   }
  } catch {
   return $false
  }
 }

 for ($rep = $Start; $rep -lt ($Start + $Count); $rep++) {
  $repCsv = Join-Path $Out ("rep-{0:D4}\h1_exact_replications.csv" -f $rep)
  if (-not (Test-Path $repCsv)) { return $false }
  if ((Get-Item $repCsv).Length -le 0) { return $false }
  try {
   $rows = @(Import-Csv $repCsv)
   if ($rows.Count -ne 1) { return $false }
   if ([int]$rows[0].replication -ne $rep) { return $false }
  } catch {
   return $false
  }
 }
 return $true
}

$tasks = [System.Collections.Generic.List[object]]::new()
$expectedChunks = [System.Collections.Generic.List[object]]::new()
foreach ($n in @($config.candidate_couples)) {
 foreach ($c in @($config.compliance_rates)) {
  foreach ($m in @($config.missingness_strengths)) {
   foreach ($truth in @($config.truth_scenarios.PSObject.Properties.Name)) {
    for ($start=0; $start -lt $Replications; $start += $ChunkSize) {
     $tagC = ("{0:F2}" -f [double]$c).Replace(".","p")
     $tagM = ("{0:G}" -f [double]$m).Replace(".","p")
     $out = Join-Path $OutputRoot ("chunks\n{0}-c{1}-m{2}-{3}-r{4:D4}" -f $n,$tagC,$tagM,$truth,$start)
     $count = [Math]::Min($ChunkSize, $Replications - $start)
     $chunk = [pscustomobject]@{
      N=[int]$n; C=[double]$c; M=[double]$m; Truth=$truth
      Start=$start; Count=$count; Out=$out
     }
     $expectedChunks.Add($chunk)
     if (-not (Test-H1ChunkComplete -Out $out -Start $start -Count $count)) {
      if (Test-Path (Join-Path $out "_COMPLETE")) {
       Write-Warning "Invalid completed chunk will be recomputed: $out"
      }
      $tasks.Add($chunk)
     }
    }
   }
  }
 }
}

Write-Host "ARC H1 exact Monte Carlo"
Write-Host "Logical processors: $([Environment]::ProcessorCount); workers: $Workers; chunk size: $ChunkSize; pending chunks: $($tasks.Count)"
Write-Host "The statsmodels GEE estimator is CPU-bound; parallelism is process-level across deterministic chunks."

$running=@(); $done=0
foreach ($t in $tasks) {
 while ($running.Count -ge $Workers) {
  $finished=Wait-Job -Job $running -Any
  Receive-Job $finished -ErrorAction Continue | Write-Host
  if ($finished.State -ne "Completed") { throw "Worker failed: $($finished.Name)" }
  Remove-Job $finished
  $running=@($running | Where-Object Id -ne $finished.Id)
  $done++
  Write-Progress -Activity "H1 Monte Carlo" -Status "$done / $($tasks.Count) chunks" -PercentComplete (100*$done/[Math]::Max(1,$tasks.Count))
 }
 $running += Start-Job -Name ("H1-{0}-{1}-{2}" -f $t.Truth,$t.N,$t.Start) -ArgumentList @(
  $RepoRoot,$Python,$configPath,$t.Out,$t.N,$t.C,$t.M,$t.Truth,$t.Start,$t.Count,$MaxAttempts
 ) -ScriptBlock {
  param($root,$python,$config,$out,$n,$c,$m,$truth,$start,$count,$maxAttempts)
  Set-Location $root
  $env:OPENBLAS_NUM_THREADS = "1"
  $env:OMP_NUM_THREADS = "1"
  $env:MKL_NUM_THREADS = "1"
  $env:NUMEXPR_NUM_THREADS = "1"
  $env:VECLIB_MAXIMUM_THREADS = "1"
  function Invoke-H1Process {
   param(
    [string]$outputDir,
    [int]$repStart,
    [int]$repCount,
    [string]$logPath
   )
   $cmd = "`"$python`" manuscripts/MSC-ATTACH-P01/analysis/h1_exact_monte_carlo.py --config `"$config`" --output-dir `"$outputDir`" --couples $n --compliance $c --missingness $m --truth $truth --rep-start $repStart --replications $repCount > `"$logPath`" 2>&1"
   & cmd.exe /d /s /c $cmd
   return [int]$LASTEXITCODE
  }

  # A chunk preserves the existing 10-replication output grid, but each
  # replication is executed in a fresh Python process. This prevents
  # process-lifetime corruption while keeping resumability compatible with
  # already completed chunks.
  if (Test-Path $out) { Remove-Item -Recurse -Force $out }
  New-Item -ItemType Directory -Force -Path $out | Out-Null

  for ($rep = $start; $rep -lt ($start + $count); $rep++) {
   $repOut = Join-Path $out ("rep-{0:D4}" -f $rep)
   $repSuccess = $false
   for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
    if (Test-Path $repOut) { Remove-Item -Recurse -Force $repOut }
    New-Item -ItemType Directory -Force -Path $repOut | Out-Null
    $repLog = Join-Path $repOut ("attempt-{0}.log" -f $attempt)
    $exitCode = Invoke-H1Process -outputDir $repOut -repStart $rep -repCount 1 -logPath $repLog
    $repCsv = Join-Path $repOut "h1_exact_replications.csv"
    if ($exitCode -eq 0 -and (Test-Path $repCsv) -and ((Get-Item $repCsv).Length -gt 0)) {
     $repSuccess = $true
     if (Test-Path $repLog) { Get-Content $repLog | Write-Output }
     break
    }
    Write-Warning "Isolated H1 replication failed: N=$n truth=$truth rep=$rep attempt=$attempt/$maxAttempts exit=$exitCode log=$repLog"
   }
   if (-not $repSuccess) {
    throw "Simulation failed after isolated retries: N=$n truth=$truth rep=$rep"
   }
  }

  New-Item -ItemType File -Force -Path (Join-Path $out "_COMPLETE") | Out-Null

 }
}
if ($running.Count -gt 0) {
 Wait-Job -Job $running | Out-Null
 foreach ($job in $running) {
  Receive-Job $job -ErrorAction Continue | Write-Host
  if ($job.State -ne "Completed") { throw "Worker failed: $($job.Name)" }
  Remove-Job $job
 }
}
Write-Progress -Activity "H1 Monte Carlo" -Completed

# Build the merge manifest only from the current expected chunk grid.
# Historical/incomplete artifacts from older runner versions are ignored.
$inputs = [System.Collections.Generic.List[string]]::new()
foreach ($chunk in $expectedChunks) {
 if (-not (Test-H1ChunkComplete -Out $chunk.Out -Start $chunk.Start -Count $chunk.Count)) {
  throw "Expected chunk failed integrity validation: $($chunk.Out)"
 }

 $batchCsv = Join-Path $chunk.Out "h1_exact_replications.csv"
 if ((Test-Path $batchCsv) -and ((Get-Item $batchCsv).Length -gt 0)) {
  $inputs.Add((Resolve-Path $batchCsv).Path)
  continue
 }

 for ($rep = $chunk.Start; $rep -lt ($chunk.Start + $chunk.Count); $rep++) {
  $repCsv = Join-Path $chunk.Out ("rep-{0:D4}\h1_exact_replications.csv" -f $rep)
  if (-not (Test-Path $repCsv)) {
   throw "Missing isolated replication output: $repCsv"
  }
  if ((Get-Item $repCsv).Length -le 0) {
   throw "Empty isolated replication output: $repCsv"
  }
  $inputs.Add((Resolve-Path $repCsv).Path)
 }
}
if ($inputs.Count -eq 0) { throw "No current-grid result chunks found." }
$merged=Join-Path $OutputRoot "merged"
New-Item -ItemType Directory -Force -Path $merged | Out-Null
$inputList = Join-Path $merged "h1_chunk_inputs.txt"
$inputs | Set-Content -Path $inputList -Encoding UTF8
& $Python manuscripts/MSC-ATTACH-P01/analysis/merge_h1_exact_results.py --input-list $inputList --output-dir $merged --expected-replications $Replications
if ($LASTEXITCODE -ne 0) { throw "Strict merge failed." }
if (-not $SkipPostMergeAnalyses) {
 $decisions=Join-Path $OutputRoot "decisions"
 & $Python manuscripts/MSC-ATTACH-P01/analysis/h1_decision_analysis.py --input (Join-Path $merged "h1_exact_replications.csv") --config $configPath --output-dir $decisions
 if ($LASTEXITCODE -ne 0) { throw "Legacy decision analysis failed." }

 $inference=Join-Path $OutputRoot "inference"
 & $Python manuscripts/MSC-ATTACH-P01/analysis/h1_inference_analysis.py --input (Join-Path $merged "h1_exact_replications.csv") --config $configPath --output-dir $inference
 if ($LASTEXITCODE -ne 0) { throw "Revised H1 inference analysis failed." }
} else {
 Write-Host "Post-merge legacy/revised H1 analyses skipped for focused validation."
}

Write-Host "Completed. Results: $OutputRoot"
