#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

$SkillRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$OutDir = Join-Path $SkillRoot "references/generated"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$version = m365 version
$topHelp = m365 --help
$topHelp | Set-Content -Path (Join-Path $OutDir "m365-help.txt") -Encoding utf8

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
    $help | Set-Content -Path $path -Encoding utf8
    $index += ('- `{0}` -> `references/generated/{0}-help.txt`' -f $group)
}

$index | Set-Content -Path (Join-Path $OutDir "index.md") -Encoding utf8
