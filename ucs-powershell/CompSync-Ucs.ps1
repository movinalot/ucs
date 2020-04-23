<# CompSync-Ucs.ps1
Purpose:
    UCS Manager Compare and Sync
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true, HelpMessage = "Enter Source UCS Manager Hostname or IP address")]
  [string] $SourceUcsHost,
    
  [Parameter(Mandatory = $true, HelpMessage = "Enter Source UCS Manager user")]
  [string] $SourceUcsUser,
    
  [Parameter(Mandatory = $true, HelpMessage = "Enter Source UCS Manager user's Password")]
  [string] $SourceUcsPass,

  [Parameter(Mandatory = $true, HelpMessage = "Enter Target UCS Manager Hostname or IP address")]
  [string] $TargetUcsHost,
    
  [Parameter(Mandatory = $true, HelpMessage = "Enter Target UCS Manager user")]
  [string] $TargetUcsUser,
    
  [Parameter(Mandatory = $true, HelpMessage = "Enter Target UCS Manager user's Password")]
  [string] $TargetUcsPass

)

Import-Module -Name Cisco.UCSManager

$sourceCredentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $SourceUcsUser, $(convertto-securestring -Force -AsPlainText $SourceUcsPass)
$sourceUcs = Connect-Ucs -Name $SourceUcsHost -Credential $sourceCredentials -NotDefault

$targetCredentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $TargetUcsUser, $(convertto-securestring -Force -AsPlainText $TargetUcsPass)
$targetUcs = Connect-Ucs -Name $TargetUcsHost -Credential $TargetCredentials -NotDefault

$sourceOrg = Get-UcsOrg -Ucs $sourceUcs -Name root | Add-UcsOrg -Name OrgA -ModifyPresent
$targetOrg = Get-UcsOrg -Ucs $targetUcs -Name root | Add-UcsOrg -Name OrgB -ModifyPresent

$sp = Add-UcsServiceProfile -Ucs $sourceUcs -Org $sourceOrg -Name abc -ModifyPresent
$sp

$xlateDn = @{ }; $xlateDn['org-root/org-OrgA/ls-abc'] = 'org-root/org-OrgB/ls-xyz'

Compare-UcsManagedObject (Get-UcsServiceProfile -Ucs $targetUcs -Org $targetOrg -Name xyz -LimitScope)`
  (Get-UcsServiceProfile -Ucs $sourceUcs -Org $sourceOrg -Name abc -LimitScope) -XlateMap $xlateDn

Compare-UcsManagedObject (Get-UcsServiceProfile -Ucs $targetUcs -Org $targetOrg -Name xyz -LimitScope)`
  (Get-UcsServiceProfile -Ucs $sourceUcs -Org $sourceOrg -Name abc -LimitScope) -XlateMap $xlateDn

Compare-UcsManagedObject (Get-UcsServiceProfile -Ucs $targetUcs -Org $targetOrg -Name xyz -LimitScope)`
  (Get-UcsServiceProfile -Ucs $sourceUcs -Org $sourceOrg -Name abc -LimitScope) -Xlateorg org-root/org-OrgB

Sync-UcsManagedObject -Ucs $targetUcs (Compare-UcsManagedObject `
  (Get-UcsServiceProfile -Ucs $targetUcs -Org $targetOrg -Name xyz -LimitScope)`
  (Get-UcsServiceProfile -Ucs $sourceUcs -Org $sourceOrg -Name abc -LimitScope) -XlateMap $xlateDn) -WhatIf