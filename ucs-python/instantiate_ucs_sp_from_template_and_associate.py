"""
create_ucs_sp_template.py

Purpose:
    UCS Manager Instantiate a UCS Service Profile from Template and Associate
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.ls.LsBinding import LsBinding
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

SP_FROM_TEMPLATE = LsServer(
    parent_mo_or_dn='org-root/org-devnet',
    name="devcore-server-01",
    src_templ_name="devcore_template",
    type="instance"
)

LsBinding(
    parent_mo_or_dn=SP_FROM_TEMPLATE,
    pn_dn="sys/chassis-7/blade-3"
)

HANDLE.add_mo(SP_FROM_TEMPLATE, modify_present=True)
HANDLE.commit()

HANDLE.logout()
