"""
remove_ucs_bios_policy.py

Purpose:
    remove a UCS bios policy
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

from ucsmsdk.ucshandle import UcsHandle
import connection as Connection

UCS_HOST = Connection.UCS_HOST
UCS_USER = Connection.UCS_USER
UCS_PASS = Connection.UCS_PASS

def remove_ucs_bios_policy():
    """ Remove UCS BIOS Policy """
    handle = UcsHandle(UCS_HOST, UCS_USER, UCS_PASS)
    handle.login()

    mo_bios_policies = handle.query_classid("BiosVProfile")

    for mo_bios_policy in mo_bios_policies:
        if mo_bios_policy.name == "test-bios-prof":
            handle.remove_mo(mo_bios_policy)

    handle.commit()

if __name__ == '__main__':
    remove_ucs_bios_policy()
