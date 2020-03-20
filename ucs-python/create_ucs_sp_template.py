"""
create_ucs_sp_template.py

Purpose:
    UCS Manager Create a UCS Service Profile Template
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.mometa.org.OrgOrg import OrgOrg

HANDLE = UcsHandle(
    "sandbox-ucsm1.cisco.com",
    "admin",
    "password"
)

HANDLE.login()

ORG_ORG = OrgOrg(
    parent_mo_or_dn='org-root',
    name="devnet",
)
HANDLE.add_mo(ORG_ORG, modify_present=True)
HANDLE.commit()

SP_TEMPLATE = LsServer(
    parent_mo_or_dn='org-root/org-devnet',
    name="devcore_template",
    type="updating-template"
)

HANDLE.add_mo(SP_TEMPLATE, modify_present=True)
HANDLE.commit()

HANDLE.logout()
