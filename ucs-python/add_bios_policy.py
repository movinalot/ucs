"""
add_ucs_bios_policy.py

Purpose:
    add/update a UCS bios policy
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.bios.BiosVProfile import BiosVProfile
from ucsmsdk.mometa.bios.BiosVfQuietBoot import BiosVfQuietBoot
from ucsmsdk.mometa.bios.BiosVfResumeOnACPowerLoss import BiosVfResumeOnACPowerLoss
from ucsmsdk.mometa.bios.BiosVfConsoleRedirection import BiosVfConsoleRedirection
import connection as Connection

UCS_HOST = Connection.UCS_HOST
UCS_USER = Connection.UCS_USER
UCS_PASS = Connection.UCS_PASS

HANDLE = UcsHandle(UCS_HOST, UCS_USER, UCS_PASS)
HANDLE.login()