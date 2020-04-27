"""
add_vlan_to_vnic_template.py

Purpose:
    Add VLAN to VNIC Template
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf
import connection as Connection

UCS_HOST = Connection.UCS_HOST
UCS_USER = Connection.UCS_USER
UCS_PASS = Connection.UCS_PASS

def add_vlan_to_vnic_template():
    """ Add VLAN to VNIC Template """
    handle = UcsHandle(UCS_HOST, UCS_USER, UCS_PASS)
    handle.login()

    my_vlan = handle.query_classid("fabricVlan", filter_str='(id,"301")')
    my_templ = handle.query_classid("vnicLanConnTempl", filter_str='(name,"Trunk_B")')

    VnicEtherIf(
        parent_mo_or_dn=my_templ[0],
        default_net=my_vlan[0].default_net,
        name=my_vlan[0].name
    )
    handle.add_mo(my_templ[0], True)
    handle.commit()

if __name__ == '__main__':
    add_vlan_to_vnic_template()
