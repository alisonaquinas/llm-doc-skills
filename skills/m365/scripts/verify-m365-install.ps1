#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"
$env:NO_UPDATE_NOTIFIER = "1"

function Run-Check {
    param([string]$Name, [scriptblock]$Command)
    try {
        $value = & $Command
        Write-Output "OK    $Name`t$value"
    } catch {
        Write-Output "FAIL  $Name`t$($_.Exception.Message)"
        $script:Failed = $true
    }
}

$script:Failed = $false
Run-Check "node" { node --version }
Run-Check "npm" { npm --version }
Run-Check "m365 version" { m365 version --output text }
Run-Check "m365 status" { m365 status --output text }
Run-Check "m365 help" { (m365 --help | Where-Object { $_.Trim() } | Select-Object -First 1) }

if ($script:Failed) {
    exit 1
}
