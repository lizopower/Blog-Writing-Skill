param(
  [ValidateSet("codex", "claude", "claude-plugin", "claude-standalone", "cli", "all")]
  [string] $Target = "all",
  [string] $RepoUrl = "https://github.com/lizopower/Blog-Writing-Skill.git",
  [string] $SkillName = "blog-writing-skills",
  [string] $BinDir = $(Join-Path $HOME ".local\bin")
)

$ErrorActionPreference = "Stop"
$script:LastStandaloneDest = ""

function Get-Timestamp {
  Get-Date -Format "yyyyMMddHHmmss"
}

function Install-One {
  param(
    [ValidateSet("codex", "claude")]
    [string] $HostName
  )

  if ($HostName -eq "codex") {
    $base = Join-Path $HOME ".codex\skills"
  } else {
    $base = Join-Path $HOME ".claude\skills"
  }

  $dest = Join-Path $base $SkillName
  $script:LastStandaloneDest = $dest
  New-Item -ItemType Directory -Force $base | Out-Null

  if (Test-Path (Join-Path $dest ".git")) {
    $origin = ""
    try {
      $origin = (& git -C $dest remote get-url origin 2>$null).Trim()
    } catch {
      $origin = ""
    }

    if ($origin -eq $RepoUrl -or $origin -like "*lizopower/Blog-Writing-Skill*") {
      Write-Host "Updating $HostName install at $dest"
      & git -C $dest pull --ff-only
      if ($LASTEXITCODE -ne 0) { throw "git pull failed for $dest" }
      return
    }

    $backup = "$dest.backup-$(Get-Timestamp)"
    Write-Host "Existing git checkout has different origin ($origin); moving to $backup"
    Move-Item -LiteralPath $dest -Destination $backup
  } elseif (Test-Path $dest) {
    $backup = "$dest.backup-$(Get-Timestamp)"
    Write-Host "Existing copy install found; moving to $backup"
    Move-Item -LiteralPath $dest -Destination $backup
  }

  Write-Host "Installing $HostName skill to $dest"
  & git clone --depth 1 $RepoUrl $dest
  if ($LASTEXITCODE -ne 0) { throw "git clone failed for $dest" }
}

function Install-CliShim {
  param(
    [string] $SkillDir
  )

  $entry = Join-Path $SkillDir "scripts\blog-writing.py"
  if (-not (Test-Path -LiteralPath $entry)) {
    Write-Warning "CLI entry not found at $entry; skipping blog-writing shim."
    return
  }

  New-Item -ItemType Directory -Force $BinDir | Out-Null

  $cmdText = "@echo off`r`npython ""$entry"" %*`r`n"
  Set-Content -LiteralPath (Join-Path $BinDir "blog-writing.cmd") -Value $cmdText -Encoding ASCII
  Set-Content -LiteralPath (Join-Path $BinDir "bws.cmd") -Value $cmdText -Encoding ASCII

  $escapedEntry = $entry.Replace("'", "''")
  $psText = "& python '$escapedEntry' @args`n"
  Set-Content -LiteralPath (Join-Path $BinDir "blog-writing.ps1") -Value $psText -Encoding UTF8
  Set-Content -LiteralPath (Join-Path $BinDir "bws.ps1") -Value $psText -Encoding UTF8

  Write-Host "Installed CLI shim: $(Join-Path $BinDir 'blog-writing.cmd')"
  Write-Host "Alias installed: $(Join-Path $BinDir 'bws.cmd')"

  $pathParts = ($env:PATH -split ';') | Where-Object { $_ }
  if ($pathParts -notcontains $BinDir) {
    Write-Host "NOTE: add $BinDir to PATH to run 'blog-writing init' from any directory."
  }
}

function Install-ClaudePlugin {
  if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    throw "claude CLI not found. Use target 'claude-standalone' for a filesystem skill install."
  }

  Write-Host "Adding/updating Claude Code marketplace source"
  & claude plugin marketplace add lizopower/Blog-Writing-Skill
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Marketplace add returned a non-zero exit code; continuing in case it is already configured."
  }

  Write-Host "Installing/updating Claude Code plugin: blog-writing-skills"
  & claude plugin install blog-writing-skills
  if ($LASTEXITCODE -ne 0) {
    & claude plugin update blog-writing-skills@blog-writing-marketplace
    if ($LASTEXITCODE -ne 0) { throw "Claude plugin install/update failed" }
  }
}

switch ($Target) {
  "codex" {
    Install-One "codex"
    Install-CliShim $script:LastStandaloneDest
  }
  "claude" { Install-ClaudePlugin }
  "claude-plugin" { Install-ClaudePlugin }
  "cli" {
    $repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
    Install-CliShim $repoRoot
  }
  "claude-standalone" {
    Install-One "claude"
    Install-CliShim $script:LastStandaloneDest
  }
  "all" {
    Install-One "codex"
    Install-CliShim $script:LastStandaloneDest
    Install-ClaudePlugin
  }
}

Write-Host ""
Write-Host "Done. Restart the agent or start a new session so the skill index is re-scanned."
Write-Host "For research workflows, also verify Tavily with: tvly --status"
