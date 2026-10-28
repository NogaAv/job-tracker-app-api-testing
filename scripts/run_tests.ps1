#!/usr/bin/env pwsh
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonBin = if ($env:PYTHON_BIN) { $env:PYTHON_BIN } else {
    $venvPython = Join-Path $scriptDir '.venv\Scripts\python.exe'
    if (Test-Path $venvPython) {
        $venvPython
    } elseif (Get-Command py -ErrorAction SilentlyContinue) {
        'py'
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        'python'
    } else {
        throw 'Python executable not found in PATH or .venv.'
    }
}

if ($pythonBin -eq 'py') {
    & py -3 (Join-Path $scriptDir 'run_tests.py') @Args
} else {
    & $pythonBin (Join-Path $scriptDir 'run_tests.py') @Args
}
exit $LASTEXITCODE
