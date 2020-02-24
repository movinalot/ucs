function UCSM_LAN_Uplink
{
 
    Write-Host "Configuring LAN and Server uplinks on $UCSM_Domain" -ForegroundColor Yellow

    $fabrics = @("A", "B")

    #Add UCS FI Uplinks on FIA and FIB
    $ports = @($(7..10))
    Start-UcsTransaction
    foreach($fabric in $fabrics) {
        foreach($port in $ports) {
            add-ucsuplinkport -filancloud $fabric -portid $port -slotid 1 -ucs $ucsDomain
        }
    }
    Complete-UcsTransaction

    #Add UCS FI Server Uplinks on FIA and FIB
    $ports = @($(17..40))
    Start-UcsTransaction
    foreach($fabric in $fabrics) {
        foreach($port in $ports) {
            add-ucsserverport -fabricservercloud $fabric -portid $port -slotid 1 -ucs $ucsDomain
        }
    }
    Complete-UcsTransaction

    #Add LAN Port Channel
    $ports = @($(7..10))
    $A_PC = Get-UcsFabricApplianceCloud -Id A | Add-UcsAppliancePortChannel -PortId $PO_A  -ucs $ucsDomain
    Start-UcsTransaction
    $ports | %{Add-UcsAppliancePortChannelMember -AppliancePortChannel $A_PC -SlotId 1 -PortId $_}
    Complete-UcsTransaction

    $B_PC = Get-UcsFabricApplianceCloud -Id B | Add-UcsAppliancePortChannel -PortId $PO_B  -ucs $ucsDomain
    Start-UcsTransaction
    $ports| %{Add-UcsAppliancePortChannelMember -AppliancePortChannel $B_PC -SlotId 1 -PortId $_}
    Complete-UcsTransaction
}
