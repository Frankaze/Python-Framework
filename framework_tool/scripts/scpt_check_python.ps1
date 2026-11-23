# Check Python code with the Ruff version pinned in framework_tool.
# Usage (any directory):
#   <framework>\framework_tool\scripts\scpt_check_python.ps1 [-Path <dir>] [-Fix]
# Examples from a product root next to python-framework:
#   ..\python-framework\framework_tool\scripts\scpt_check_python.ps1
#   ..\python-framework\framework_tool\scripts\scpt_check_python.ps1 -Path src\ileague_api -Fix
#
# Without -Fix: ruff check and ruff format --check; nothing is modified.
# With -Fix: ruff check --fix, then ruff format.
# Rules come from the ruff.toml found above each checked file, which extends
# framework_tool/ruff.toml. Exits with 1 when any step fails.

param(
    [string]$Path = '.',
    [switch]$Fix
)

$ErrorActionPreference = 'Stop'

$strToolDir = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$strTarget = (Resolve-Path $Path).Path

if ($Fix) {
    $lstSteps = @(
        @('check', '--fix', $strTarget),
        @('format', $strTarget)
    )
}
else {
    $lstSteps = @(
        @('check', $strTarget),
        @('format', '--check', $strTarget)
    )
}

$intFailed = 0
foreach ($lstArgs in $lstSteps) {
    Write-Host "ruff $($lstArgs -join ' ')"
    uv run --project $strToolDir ruff @lstArgs
    if ($LASTEXITCODE -ne 0) {
        $intFailed += 1
    }
}

if ($intFailed -gt 0) {
    exit 1
}
