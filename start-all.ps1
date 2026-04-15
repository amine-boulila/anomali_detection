param(
    [switch]$Install
)

$ErrorActionPreference = "Stop"

function Find-CommandPath {
    param(
        [string[]]$Candidates
    )

    foreach ($candidate in $Candidates) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command) {
            return $command.Source
        }
    }

    return $null
}

function Get-ProjectPath {
    return Split-Path -Parent $MyInvocation.MyCommand.Path
}

$projectRoot = Get-ProjectPath
$serverPath = Join-Path $projectRoot "server"
$clientPath = Join-Path $projectRoot "client"

$npmPath = Find-CommandPath -Candidates @("npm.cmd", "npm")
$pythonPath = Find-CommandPath -Candidates @("python", "py", "python3")

if (-not (Test-Path $serverPath)) {
    throw "The 'server' folder was not found at: $serverPath"
}

if (-not (Test-Path $clientPath)) {
    throw "The 'client' folder was not found at: $clientPath"
}

if (-not $npmPath) {
    throw "npm was not found. Please install Node.js first."
}

if (-not $pythonPath) {
    throw "Python was not found. Please install Python and make sure it is available in PATH."
}

$venvActivate = Join-Path $projectRoot ".venv\Scripts\Activate.ps1"

$backendSetup = @()
if (Test-Path $venvActivate) {
    $backendSetup += "& '$venvActivate'"
}

if ($Install) {
    $backendSetup += "& '$pythonPath' -m pip install -r requirements.txt"
}

$backendSetup += "& '$pythonPath' -m uvicorn main:app --reload"
$backendCommand = ($backendSetup -join "; ")

$frontendSetup = @()
if ($Install) {
    $frontendSetup += "& '$npmPath' install"
}

$frontendSetup += "& '$npmPath' run dev"
$frontendCommand = ($frontendSetup -join "; ")

Write-Host "Starting backend in a new PowerShell window..." -ForegroundColor Green
Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$serverPath'; $backendCommand"
)

Start-Sleep -Seconds 2

Write-Host "Starting frontend in a new PowerShell window..." -ForegroundColor Green
Start-Process powershell.exe -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$clientPath'; $frontendCommand"
)

Write-Host ""
Write-Host "Done." -ForegroundColor Green
Write-Host "Backend:  http://127.0.0.1:8000"
Write-Host "Frontend: http://localhost:5173"
Write-Host ""
Write-Host "Tips:"
Write-Host "- Run '.\start-all.ps1' to start both apps."
Write-Host "- Run '.\start-all.ps1 -Install' the first time to install dependencies before starting."
