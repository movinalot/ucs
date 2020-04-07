<# Set-Imc-Snmp.ps1
Purpose:
    IMC SNMP Example
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true,HelpMessage="Enter IMC hostname or IP address")]
    [string] $ImcHost,
    
  [Parameter(Mandatory=$true,HelpMessage="Enter IMC user")]
    [string] $ImcUser,
  
  [Parameter(Mandatory=$true,HelpMessage="Enter IMC user's Password")]
    [string] $ImcPass
)

Import-Module -Name Cisco.Imc

$credentials = new-object -typename System.Management.Automation.PSCredential -argumentlist $ImcUser,$(convertto-securestring -Force -AsPlainText $ImcPass)

Connect-Imc -Name $ImcHost -Credential $credentials

Set-Imcsnmp -AdminState enabled -Community commstring -Force
Get-ImcSnmpTrap -Id 1 | Set-ImcSnmpTrap -AdminState enabled -Hostname 10.10.10.10 -Version v2c -Force

Disconnect-Imc
