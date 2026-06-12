param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]] $InstallerArgs
)

$ErrorActionPreference = "Stop"
$installer = Join-Path $PSScriptRoot "scripts\install.ps1"

if ($InstallerArgs.Count -eq 0) {
  & $installer cli
} else {
  & $installer @InstallerArgs
}

exit $LASTEXITCODE
