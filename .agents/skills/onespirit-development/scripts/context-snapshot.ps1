param(
    [ValidateSet("summary", "backend", "frontend", "docs", "runtime", "full")]
    [string]$Scope = "summary",
    [ValidateRange(1, 20)]
    [int]$TopFiles = 8
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Get-CommandValue {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Command,
        [string[]]$Arguments = @()
    )

    if (-not (Get-Command $Command -ErrorAction SilentlyContinue)) {
        return "not found"
    }

    $output = @(& $Command @Arguments 2>$null)
    if ($LASTEXITCODE -ne 0 -or $output.Count -eq 0) {
        return "unavailable"
    }

    return (($output -join " ").Trim())
}

function Write-RuntimeSnapshot {
    Write-Output ""
    Write-Output "Runtime toolchain:"
    Write-Output "  Docker: $(Get-CommandValue -Command "docker" -Arguments @("--version"))"
    Write-Output "  Docker Compose: $(Get-CommandValue -Command "docker" -Arguments @("compose", "version"))"
    Write-Output "  Node: $(Get-CommandValue -Command "node" -Arguments @("--version"))"
    Write-Output "  npm: $(Get-CommandValue -Command "npm" -Arguments @("--version"))"
    Write-Output "  Python: $(Get-CommandValue -Command "python" -Arguments @("--version"))"

    Write-Output ""
    Write-Output "Local dependency state:"
    Write-Output "  backend/.venv: $(if (Test-Path "backend/.venv/Scripts/python.exe") { "installed" } else { "missing" })"
    Write-Output "  frontend/node_modules: $(if (Test-Path "frontend/node_modules") { "installed" } else { "missing" })"
    Write-Output "  frontend/package-lock.json: $(if (Test-Path "frontend/package-lock.json") { "present" } else { "missing" })"
    Write-Output "  backend/requirements.txt: $(if (Test-Path "backend/requirements.txt") { "present" } else { "missing" })"

    Write-Output ""
    Write-Output "Docker Compose services:"
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Output "  docker command not found"
    }
    else {
        $services = @(& docker compose ps --format json 2>$null)
        if ($LASTEXITCODE -ne 0 -or $services.Count -eq 0) {
            Write-Output "  no compose service data available"
        }
        else {
            foreach ($serviceLine in $services) {
                if ([string]::IsNullOrWhiteSpace($serviceLine)) {
                    continue
                }

                $service = $serviceLine | ConvertFrom-Json
                $health = if ($service.Health) { $service.Health } else { "n/a" }
                $ports = if ($service.Ports) { $service.Ports } else { "no published ports" }
                Write-Output ("  {0}: {1}; health={2}; ports={3}" -f $service.Service, $service.State, $health, $ports)
            }
        }
    }

    Write-Output ""
    Write-Output "Dependency verification commands:"
    Write-Output "  backend local: cd backend; .venv\Scripts\python.exe -m pip check"
    Write-Output "  backend container: docker compose exec -T backend python -m pip check"
    Write-Output "  frontend local: cd frontend; npm ls --depth=0; npm audit"
}

$repoRoot = (& git rev-parse --show-toplevel).Trim()
if (-not $repoRoot) {
    throw "Run this script inside the OneSpirit git repository."
}

Push-Location $repoRoot
try {
    Write-Output "=== OneSpirit context snapshot ==="
    Write-Output "Root: $repoRoot"
    Write-Output "Branch: $((& git branch --show-current).Trim())"
    Write-Output "Head: $((& git log -1 --pretty=format:'%h %s').Trim())"

    $status = @(& git status --short)
    if ($status.Count -eq 0) {
        Write-Output "Working tree: clean"
    }
    else {
        Write-Output "Working tree:"
        $status | ForEach-Object { Write-Output "  $_" }
    }

    Write-Output ""
    Write-Output "Frontend scripts:"
    $package = Get-Content "frontend/package.json" -Raw | ConvertFrom-Json
    $package.scripts.PSObject.Properties |
        Sort-Object Name |
        ForEach-Object { Write-Output "  $($_.Name): $($_.Value)" }

    Write-Output ""
    Write-Output "Backend validation: python -m pytest app/tests -q; python -m pip check"

    if ($Scope -in @("backend", "full")) {
        Write-Output ""
        Write-Output "Backend modules:"
        Get-ChildItem "backend/app/modules" -Directory |
            Sort-Object Name |
            ForEach-Object { Write-Output "  $($_.Name)" }
        Write-Output "Backend tests: $((Get-ChildItem 'backend/app/tests/test_*.py').Count)"
    }

    if ($Scope -in @("frontend", "full")) {
        Write-Output ""
        Write-Output "Largest frontend source files:"
        Get-ChildItem "frontend/src" -Recurse -File -Include *.vue,*.js,*.css |
            ForEach-Object {
                [PSCustomObject]@{
                    Lines = (Get-Content $_.FullName | Measure-Object -Line).Lines
                    Path = $_.FullName.Substring($repoRoot.Length + 1)
                }
            } |
            Sort-Object Lines -Descending |
            Select-Object -First $TopFiles |
            ForEach-Object { Write-Output ("  {0,5}  {1}" -f $_.Lines, $_.Path) }
    }

    if ($Scope -in @("docs", "full")) {
        Write-Output ""
        Write-Output "Current documented status:"
        Select-String -Path "PROJECT_CONTEXT.md", "README.md" -Pattern "Status Project|^\| Status \|" |
            ForEach-Object { Write-Output "  $($_.Path):$($_.LineNumber) $($_.Line.Trim())" }
        Write-Output "Recent sprint headings:"
        Select-String -Path "SPRINT_LOG.md" -Pattern "^## Sprint " |
            Select-Object -Last 5 |
            ForEach-Object { Write-Output "  $($_.Line)" }
    }

    if ($Scope -in @("runtime", "full")) {
        Write-RuntimeSnapshot
    }

    if ($Scope -eq "full") {
        Write-Output ""
        Write-Output "Tracked file counts:"
        $tracked = @(& git ls-files)
        Write-Output "  all: $($tracked.Count)"
        Write-Output "  Python: $((@($tracked | Where-Object { $_ -like '*.py' })).Count)"
        Write-Output "  frontend JS/Vue: $((@($tracked | Where-Object { $_ -like '*.js' -or $_ -like '*.vue' })).Count)"
        Write-Output "  Markdown: $((@($tracked | Where-Object { $_ -like '*.md' })).Count)"
    }
}
finally {
    Pop-Location
}
