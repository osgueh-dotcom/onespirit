<#
.SYNOPSIS
Runs a local Microsoft Edge CDP smoke test for OneSpirit Workflow.

.DESCRIPTION
Starts Microsoft Edge with a temporary profile and remote debugging port, uses
the Chrome DevTools Protocol over WebSocket, logs in through the backend API,
opens the local frontend, and verifies the Projects creation modal at desktop
and mobile viewport sizes. With an admin-capable login it also provisions local
smoke users and verifies role-aware menu and route visibility. Secrets are read
from environment variables or parameters but are never printed.

.EXAMPLE
$env:EDGE_SMOKE_LOGIN_EMAIL = "admin@onespirit.asia"
$env:EDGE_SMOKE_LOGIN_PASSWORD = "<password-from-secure-channel>"
powershell -ExecutionPolicy Bypass -File scripts/edge-local-smoke.ps1
Remove-Item Env:EDGE_SMOKE_LOGIN_PASSWORD
#>

[CmdletBinding()]
param(
    [string]$FrontendUrl = $env:EDGE_SMOKE_FRONTEND_URL,
    [string]$BackendUrl = $env:EDGE_SMOKE_BACKEND_URL,
    [string]$LoginEmail = $env:EDGE_SMOKE_LOGIN_EMAIL,
    [string]$LoginPassword = $env:EDGE_SMOKE_LOGIN_PASSWORD,
    [string]$EdgePath = $env:EDGE_PATH,
    [switch]$Headful,
    [switch]$Json,
    [switch]$SkipAuth,
    [switch]$SkipRoleMatrix
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $PSScriptRoot "edge-local-smoke.mjs"
if (-not (Test-Path -LiteralPath $scriptPath)) {
    Write-Error "Missing smoke script: $scriptPath"
}

$node = Get-Command node -ErrorAction SilentlyContinue
if ($null -eq $node) {
    Write-Error "Node.js is required for the Edge CDP smoke test."
}

$arguments = @($scriptPath)

if (-not [string]::IsNullOrWhiteSpace($FrontendUrl)) {
    $arguments += @("--frontend-url", $FrontendUrl)
}

if (-not [string]::IsNullOrWhiteSpace($BackendUrl)) {
    $arguments += @("--backend-url", $BackendUrl)
}

if (-not [string]::IsNullOrWhiteSpace($LoginEmail)) {
    $arguments += @("--email", $LoginEmail)
}

if (-not [string]::IsNullOrWhiteSpace($EdgePath)) {
    $arguments += @("--edge-path", $EdgePath)
}

if ($Headful) {
    $arguments += "--headful"
}

if ($Json) {
    $arguments += "--json"
}

if ($SkipAuth) {
    $arguments += "--skip-auth"
}

if ($SkipRoleMatrix) {
    $arguments += "--skip-role-matrix"
}

if (-not [string]::IsNullOrWhiteSpace($LoginPassword)) {
    $env:EDGE_SMOKE_LOGIN_PASSWORD = $LoginPassword
}

& $node.Source @arguments
exit $LASTEXITCODE
