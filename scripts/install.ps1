param(
  [ValidateSet("codex", "claude", "all")]
  [string] $Target = "all",
  [string] $RepoUrl = "https://github.com/lizopower/Blog-Writing-Skill.git",
  [string] $SkillName = "blog-writing-skills"
)

$ErrorActionPreference = "Stop"

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

switch ($Target) {
  "codex" { Install-One "codex" }
  "claude" { Install-One "claude" }
  "all" {
    Install-One "codex"
    Install-One "claude"
  }
}

Write-Host ""
Write-Host "Done. Restart the agent or start a new session so the skill index is re-scanned."
Write-Host "For research workflows, also verify Tavily with: tvly --status"
