# Copyright (c) 2026 haoxuanjng-lang. SPDX-License-Identifier: MIT
[CmdletBinding()]
param(
    [ValidatePattern('^([01]\d|2[0-3]):[0-5]\d$')]
    [string]$At = '09:00',
    [string]$TaskName = 'Kaggle-Solutions-Skills-Daily-Agent',
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonPath = (Get-Command python -ErrorAction Stop).Source
$backgroundPython = Join-Path (Split-Path -Parent $pythonPath) 'pythonw.exe'
if (Test-Path -LiteralPath $backgroundPython) { $pythonPath = $backgroundPython }
$null = Get-Command codex -ErrorAction Stop
$taskRunner = Join-Path $PSScriptRoot 'run_daily_agent.py'
$localTimezone = Get-TimeZone
if ($localTimezone.Id -ne 'China Standard Time' -and $localTimezone.Id -ne 'Asia/Shanghai') {
    throw 'This task uses local wall-clock time. Set a Shanghai schedule appropriate to this machine timezone before installing.'
}
$taskUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument "`"$taskRunner`" --execute" -WorkingDirectory $projectRoot
$trigger = New-ScheduledTaskTrigger -Daily -At $At
$principal = New-ScheduledTaskPrincipal -UserId $taskUser -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -MultipleInstances IgnoreNew -ExecutionTimeLimit ([TimeSpan]::Zero)
if (-not $DryRun) {
    Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description 'Authorized daily Kaggle Solutions Skills development and maintenance via Codex; project-only, logged isolated worktrees.' -Force | Out-Null
}
[ordered]@{
    dry_run = [bool]$DryRun
    task_name = $TaskName
    daily_at = $At
    timezone = 'Asia/Shanghai'
    executable = $pythonPath
    arguments = $action.Arguments
    project = $projectRoot
    requires_user_logged_in = $true
    logs = (Join-Path $projectRoot 'cache\maintenance\runs')
} | ConvertTo-Json
