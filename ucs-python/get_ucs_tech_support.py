"""
get_ucs_tech_support.py

Purpose:
    Create and download a UCS Tech Support
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.utils.ucstechsupport import get_tech_support
import connection as Connection

UCS_HOST = Connection.UCS_HOST
UCS_USER = Connection.UCS_USER
UCS_PASS = Connection.UCS_PASS


def proess_tech_support():
    """ Create and download a UCS Tech Support """
    handle = UcsHandle(UCS_HOST, UCS_USER, UCS_PASS)
    handle.login()

    get_tech_support(
        handle=handle,
        option="ucsm-mgmt",
        file_dir='.',
        file_name="ucsm.tar",
        timeout=1800
    )

    handle.logout()


if __name__ == '__main__':
    proess_tech_support()
