<#
.SYNOPSIS
Runs a dev tunnel smoke test for OneSpirit Workflow.

.DESCRIPTION
Checks the forwarded frontend, frontend-to-backend API proxy, login, current user,
and direct backend health. Secrets are read from environment variables or
parameters but are never printed.

.EXAMPLE
$env:SMOKE_FRONTEND_URL = "https://example-5173.asse.devtunnels.ms"
$env:SMOKE_BACKEND_URL = "https://example-8000.asse.devtunnels.ms"
$env:SMOKE_LOGIN_EMAIL = "demo@onespirit.asia"
$env:SMOKE_LOGIN_PASSWORD = "<demo-password-from-secure-channel>"
powershell -ExecutionPolicy Bypass -File scripts/dev-tunnel-smoke.ps1
#>

[CmdletBinding()]
param(
    [string]$FrontendUrl = $env:SMOKE_FRONTEND_URL,
    [string]$BackendUrl = $env:SMOKE_BACKEND_URL,
    [string]$LoginEmail = $env:SMOKE_LOGIN_EMAIL,
    [string]$LoginPassword = $env:SMOKE_LOGIN_PASSWORD,
    [string]$FrontendPath = $env:SMOKE_FRONTEND_PATH,
    [switch]$Json
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($LoginEmail)) {
    $LoginEmail = "demo@onespirit.asia"
}

if ([string]::IsNullOrWhiteSpace($FrontendPath)) {
    $FrontendPath = "/onespirit/"
}

function Normalize-BaseUrl {
    param([string]$Url)
    if ([string]::IsNullOrWhiteSpace($Url)) {
        return $null
    }
    return $Url.Trim().TrimEnd("/")
}

function Get-Origin {
    param([string]$Url)
    return ([System.Uri]$Url).GetLeftPart([System.UriPartial]::Authority)
}

function Join-Url {
    param(
        [string]$BaseUrl,
        [string]$Path
    )
    return "$(Normalize-BaseUrl $BaseUrl)/$($Path.TrimStart('/'))"
}

function Resolve-Url {
    param(
        [string]$Origin,
        [string]$MaybeRelativeUrl
    )

    if ($MaybeRelativeUrl -match '^https?://') {
        return $MaybeRelativeUrl
    }

    if ($MaybeRelativeUrl.StartsWith("/")) {
        return "$(Normalize-BaseUrl $Origin)$MaybeRelativeUrl"
    }

    return "$(Normalize-BaseUrl $Origin)/$MaybeRelativeUrl"
}

function Derive-BackendUrl {
    param([string]$Url)

    if ([string]::IsNullOrWhiteSpace($Url)) {
        return $null
    }

    $uri = [System.Uri]$Url
    if ($uri.Host -match '-5173\.') {
        $backendHost = $uri.Host -replace '-5173\.', '-8000.'
        return "$($uri.Scheme)://$backendHost"
    }

    if (-not $uri.IsDefaultPort -and $uri.Port -eq 5173) {
        $builder = [System.UriBuilder]$uri
        $builder.Port = 8000
        $builder.Path = ""
        $builder.Query = ""
        return $builder.Uri.GetLeftPart([System.UriPartial]::Authority)
    }

    return $null
}

$FrontendUrl = Normalize-BaseUrl $FrontendUrl
if ([string]::IsNullOrWhiteSpace($FrontendUrl)) {
    Write-Error "SMOKE_FRONTEND_URL or -FrontendUrl is required."
}

if ([string]::IsNullOrWhiteSpace($BackendUrl)) {
    $BackendUrl = Derive-BackendUrl $FrontendUrl
} else {
    $BackendUrl = Normalize-BaseUrl $BackendUrl
}

$frontendOrigin = Get-Origin $FrontendUrl
$checks = New-Object System.Collections.Generic.List[object]

function Add-Check {
    param(
        [string]$Name,
        [bool]$Ok,
        [string]$Detail
    )

    $script:checks.Add([pscustomobject]@{
        name = $Name
        ok = $Ok
        detail = $Detail
    })
}

function Get-ExceptionStatusCode {
    param([object]$ErrorRecord)

    $exception = $ErrorRecord.Exception
    $responseProperty = $exception.PSObject.Properties["Response"]
    if ($null -eq $responseProperty -or $null -eq $responseProperty.Value) {
        return $null
    }

    $statusProperty = $responseProperty.Value.PSObject.Properties["StatusCode"]
    if ($null -eq $statusProperty -or $null -eq $statusProperty.Value) {
        return $null
    }

    return [int]$statusProperty.Value
}

function Invoke-SmokeRequest {
    param(
        [string]$Url,
        [string]$Method = "GET",
        [hashtable]$Headers = @{},
        [string]$Body = $null,
        [string]$ContentType = $null
    )

    $parameters = @{
        Uri = $Url
        Method = $Method
        UseBasicParsing = $true
        TimeoutSec = 30
        MaximumRedirection = 5
        Headers = $Headers
    }

    if ($PSBoundParameters.ContainsKey("Body")) {
        $parameters["Body"] = $Body
    }
    if ($PSBoundParameters.ContainsKey("ContentType") -and -not [string]::IsNullOrWhiteSpace($ContentType)) {
        $parameters["ContentType"] = $ContentType
    }

    return Invoke-WebRequest @parameters
}

$frontendPageUrl = Join-Url $frontendOrigin $FrontendPath
$apiBaseUrl = Join-Url $frontendOrigin "/api/v1"
$token = $null

try {
    $response = Invoke-SmokeRequest -Url $frontendPageUrl
    $title = [regex]::Match($response.Content, '<title>(.*?)</title>').Groups[1].Value
    Add-Check "frontend_load" ($response.StatusCode -eq 200 -and $response.Content -match '<div id="app"') "status=$($response.StatusCode); title=$title"

    $scriptSrcs = @()
    foreach ($match in [regex]::Matches($response.Content, '<script[^>]+src="([^"]+)"')) {
        $scriptSrcs += $match.Groups[1].Value
    }

    $assetFailures = @()
    foreach ($src in $scriptSrcs) {
        $assetUrl = Resolve-Url $frontendOrigin $src
        try {
            $assetResponse = Invoke-SmokeRequest -Url $assetUrl
            if ($assetResponse.StatusCode -ne 200 -or $assetResponse.Content.Length -lt 10) {
                $assetFailures += "$src status=$($assetResponse.StatusCode) bytes=$($assetResponse.Content.Length)"
            }
        } catch {
            $assetFailures += "$src failed"
        }
    }

    Add-Check "frontend_assets" ($scriptSrcs.Count -gt 0 -and $assetFailures.Count -eq 0) "checked=$($scriptSrcs.Count); failures=$($assetFailures -join '; ')"
} catch {
    Add-Check "frontend_load" $false $_.Exception.Message
}

try {
    $response = Invoke-SmokeRequest -Url (Join-Url $apiBaseUrl "/auth/users")
    Add-Check "api_proxy_auth_gate" $false "unexpected status=$($response.StatusCode)"
} catch {
    $statusCode = Get-ExceptionStatusCode $_
    if ($null -ne $statusCode) {
        Add-Check "api_proxy_auth_gate" ($statusCode -eq 401) "status=$statusCode"
    } else {
        Add-Check "api_proxy_auth_gate" $false $_.Exception.Message
    }
}

if ([string]::IsNullOrWhiteSpace($LoginPassword)) {
    Add-Check "api_proxy_login" $false "SMOKE_LOGIN_PASSWORD or -LoginPassword is required."
} else {
    try {
        $loginBody = "username=$([System.Uri]::EscapeDataString($LoginEmail))&password=$([System.Uri]::EscapeDataString($LoginPassword))"
        $loginResponse = Invoke-RestMethod -Uri (Join-Url $apiBaseUrl "/auth/login") -Method Post -Body $loginBody -ContentType "application/x-www-form-urlencoded" -TimeoutSec 30
        $token = $loginResponse.access_token
        Add-Check "api_proxy_login" (-not [string]::IsNullOrWhiteSpace($token) -and $loginResponse.token_type -eq "bearer") "token_received=$(-not [string]::IsNullOrWhiteSpace($token)); token_type=$($loginResponse.token_type)"
    } catch {
        $statusCode = Get-ExceptionStatusCode $_
        if ($null -ne $statusCode) {
            Add-Check "api_proxy_login" $false "status=$statusCode"
        } else {
            Add-Check "api_proxy_login" $false $_.Exception.Message
        }
    }
}

if (-not [string]::IsNullOrWhiteSpace($token)) {
    try {
        $meResponse = Invoke-RestMethod -Uri (Join-Url $apiBaseUrl "/auth/me") -Headers @{ Authorization = "Bearer $token" } -TimeoutSec 30
        Add-Check "api_proxy_current_user" (-not [string]::IsNullOrWhiteSpace($meResponse.email) -and $meResponse.is_active) "email=$($meResponse.email); role=$($meResponse.role.name); active=$($meResponse.is_active)"
    } catch {
        $statusCode = Get-ExceptionStatusCode $_
        if ($null -ne $statusCode) {
            Add-Check "api_proxy_current_user" $false "status=$statusCode"
        } else {
            Add-Check "api_proxy_current_user" $false $_.Exception.Message
        }
    }
}

if ([string]::IsNullOrWhiteSpace($BackendUrl)) {
    Add-Check "backend_health" $false "SMOKE_BACKEND_URL or -BackendUrl is required; automatic derivation failed."
} else {
    try {
        $healthResponse = Invoke-SmokeRequest -Url (Join-Url $BackendUrl "/health")
        Add-Check "backend_health" ($healthResponse.StatusCode -eq 200 -and $healthResponse.Content -match "onespirit-backend") "status=$($healthResponse.StatusCode)"
    } catch {
        $statusCode = Get-ExceptionStatusCode $_
        if ($null -ne $statusCode) {
            Add-Check "backend_health" $false "status=$statusCode"
        } else {
            Add-Check "backend_health" $false $_.Exception.Message
        }
    }
}

$allPassed = $true
foreach ($check in $checks) {
    if (-not $check.ok) {
        $allPassed = $false
        break
    }
}

$result = [pscustomobject]@{
    ok = $allPassed
    frontend_url = $FrontendUrl
    backend_url = $BackendUrl
    login_email = $LoginEmail
    checks = $checks
}

if ($Json) {
    $result | ConvertTo-Json -Depth 5
} else {
    Write-Output "OneSpirit dev tunnel smoke test"
    Write-Output "Frontend: $FrontendUrl"
    Write-Output "Backend : $BackendUrl"
    Write-Output "Login   : $LoginEmail"
    Write-Output ""

    foreach ($check in $checks) {
        $prefix = if ($check.ok) { "PASS" } else { "FAIL" }
        Write-Output "$prefix $($check.name) - $($check.detail)"
    }
}

if (-not $allPassed) {
    exit 1
}
