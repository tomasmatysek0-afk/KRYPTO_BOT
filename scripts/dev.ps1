[CmdletBinding()]
param(
    [ValidateSet("install", "install-dev", "test", "coverage", "lint", "help", "lock", "status", "no-secrets")]
    [string] $Task = "help"
)

$ErrorActionPreference = "Stop"

function Get-ProjectPython {
    if ($env:VIRTUAL_ENV) {
        return "python"
    }

    $LocalPython = Join-Path -Path (Get-Location) -ChildPath ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $LocalPython) {
        return $LocalPython
    }

    return "python"
}

function Get-ProjectTool {
    param([string] $Name)

    if ($env:VIRTUAL_ENV) {
        return $Name
    }

    $LocalTool = Join-Path -Path (Get-Location) -ChildPath ".venv\Scripts\$Name.exe"
    if (Test-Path -LiteralPath $LocalTool) {
        return $LocalTool
    }

    return $Name
}

$Python = Get-ProjectPython
$Ruff = Get-ProjectTool -Name "ruff"

switch ($Task) {
    "install" {
        # [LOCAL_VENV]
        & $Python -m pip install --upgrade pip
        # [LOCAL_VENV]
        & $Python -m pip install -e .
    }
    "install-dev" {
        # [LOCAL_VENV]
        & $Python -m pip install -e ".[dev]"
    }
    "test" {
        # [LOCAL_VENV]
        & $Python -m pytest
    }
    "coverage" {
        # [LOCAL_VENV]
        & $Python -m pytest --cov=src --cov-branch --cov-report=term-missing
    }
    "lint" {
        # [LOCAL_VENV]
        & $Ruff check .
    }
    "help" {
        # [LOCAL_VENV]
        & $Python -m coinbase_freqtrade_guarded_bot --help
    }
    "lock" {
        # [LOCAL_VENV]
        & $Python -m pip freeze --exclude-editable | Set-Content -Encoding ascii requirements-dev.lock
        # [HOST_POWERSHELL]
        Copy-Item -LiteralPath requirements-dev.lock -Destination constraints.txt -Force
    }
    "status" {
        # [HOST_POWERSHELL]
        git status --short --branch
    }
    "no-secrets" {
        # [HOST_POWERSHELL]
        $Patterns = @(
            'BEGIN (RSA|OPENSSH|EC|PRIVATE) KEY',
            ('sk' + '_live'),
            ('ghp' + '_'),
            ('xox' + '[baprs]-'),
            ('AKIA' + '[0-9A-Z]{16}'),
            ('password' + '\s*=\s*[^\s#]+'),
            ('api[_-]?' + 'secret' + '\s*=\s*[^\s#]+')
        )
        $Found = $false
        foreach ($Pattern in $Patterns) {
            rg --hidden -n -i -g '!.git/**' -g '!CODEX_MASTER_PLAN.md' -g '!.venv/**' $Pattern .
            if ($LASTEXITCODE -eq 0) {
                $Found = $true
            }
            elseif ($LASTEXITCODE -ne 1) {
                exit $LASTEXITCODE
            }
        }
        if ($Found) {
            throw "Possible secret signature found."
        }
        Write-Output "PASS no obvious secret signatures"
    }
}
