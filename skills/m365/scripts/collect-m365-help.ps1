#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"
$env:NO_UPDATE_NOTIFIER = "1"

$SkillRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$OutDir = Join-Path $SkillRoot "references/generated"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Write-Utf8LfFile {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)]$Lines
    )

    $lineArray = @($Lines) | ForEach-Object { [string]$_ }
    $content = (($lineArray -join "`n").TrimEnd("`n")) + "`n"
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $content, $utf8NoBom)
}

$version = m365 version --output text
$topHelp = m365 --help
Write-Utf8LfFile -Path (Join-Path $OutDir "m365-help.txt") -Lines $topHelp

$groups = @()
foreach ($line in $topHelp) {
    if ($line -match '^\s{2}([a-z0-9]+)\s+\*\s+') {
        $groups += $Matches[1]
    }
}

$index = @("# Generated m365 Help Snapshot", "", "- Version: $version", "- Generated: $(Get-Date -Format yyyy-MM-dd)", "")
foreach ($group in $groups) {
    $help = m365 $group --help
    $path = Join-Path $OutDir "$group-help.txt"
    Write-Utf8LfFile -Path $path -Lines $help
    $index += ('- `{0}` -> `references/generated/{0}-help.txt`' -f $group)
}

Write-Utf8LfFile -Path (Join-Path $OutDir "index.md") -Lines $index
