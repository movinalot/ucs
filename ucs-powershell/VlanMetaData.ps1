<# VlanMetaData.ps1
Purpose:
    UCS Manager Metadata example
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
#>
[CmdletBinding()]
Param(
    [Parameter(Mandatory=$true)]
    [String]
    $vlanName,
    [Parameter(Mandatory=$true)]
    [String]
    $vlanId
)
Import-Module Cisco.UCSManager

# Get the Metadata
$mo_meta = Get-UcsCmdletMeta -Noun vlan

# Extract the Allowed Vlan Name pattern
$vlan_name_pattern = $mo_meta.MoMeta.PropertyMeta |`
    Where-Object{$_.Name -eq "Name"} |`
    ForEach-Object{$_.Restriction.Pattern}

# Extract the Allowed Vlan Ids
$vlan_id_ranges = $mo_meta.MoMeta.PropertyMeta |`
    Where-Object{$_.Name -eq "Id"} |`
    ForEach-Object{$_.Restriction.Range}

"`n"
"Vlan Name and Id Restrictions"
"Vlan Name Pattern: " + $vlan_name_pattern
"Vlan Id Allowed Range: " + $vlan_id_ranges

function add_vlan
{
    Param(
        [Parameter(Mandatory=$true)]
        [String]
        $vlanName,
        [Parameter(Mandatory=$true)]
        [String]
        $vlanId
    )
    "`n"
    "Entered Vlan Name: " + $vlanName
    "Entered Vlan Name Length: " + $vlanName.Length
    "Entered Vlan Id: " + $vlanId

    if ($vlanName -notmatch "^"+$vlan_name_pattern+"$") {
        throw "$vlanName is not a valid Vlan Name - enter a name that matches this regular expression " + $vlan_name_pattern
    }

    # Empty array
    $vlan_ids = @()

    # Check for allowed Vlan Id build a list of valid ids and check if id is in list
    foreach($vlan_id_range in $vlan_id_ranges) {
        $vlan_ids += $([int]$vlan_id_range.Split('-')[0]..[int]$vlan_id_range.Split('-')[1])
    }

    if ($vlanId -notin $vlan_ids) {
        throw "$vlanId is not a valid Vlan Id, enter an Id that is in the allowed range " + $vlan_id_ranges
    }

    $creds = new-object -typename System.Management.Automation.PSCredential `
    -argumentlist $Env:UcsUser,$(convertto-securestring -Force -AsPlainText $Env:UcsPass)

    $UcsConnection = Connect-Ucs -Name $Env:UcsHost -Credential $creds
    $vlanObject = Add-Ucsvlan -LanCloud $(Get-UcsLanCloud) -Name $vlanName -id $vlanId -ModifyPresent
    $UcsConnection = Disconnect-Ucs
}

add_vlan $vlanName $vlanId