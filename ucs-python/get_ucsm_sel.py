"""
get_ucsm_sel.py

Purpose:
    UCS Manager SEL retrieval
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

import requests
import urllib3
from ucsmsdk.ucshandle import UcsHandle
import connection as Connection

UCS_HOST = Connection.UCS_HOST
UCS_USER = Connection.UCS_USER
UCS_PASS = Connection.UCS_PASS

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_ucs_sel(server_id):
    """ retrieve the server SEL """

    return requests.get(
        HANDLE.uri + "/ucsm/../operations/server-" + server_id + "/sel.txt",
        headers=GET_HEADERS,
        verify=False
        )

HANDLE = UcsHandle(UCS_HOST, UCS_USER, UCS_PASS)
HANDLE.login()

GET_HEADERS = {
    "Cookie": 'ucsm-cookie="' + HANDLE.cookie + '"'
}

# Blade Servers are two numbers, (as characters) separated by a dash
#
# e.g. chassisid-bladeid, "1-1"  "12-8"  "7-2"
#
# Rackservers are referenced by their server id (as a charater sequence)
# prefixed with "rackunit-"
#
# e.g. "rackunit-1"  "rackunit-57"  "rackunit-123"
#
# SERVERS = ["11-3", "rackunit-2"]

SERVERS = ["rackunit-7"]

for server in SERVERS:
    response = get_ucs_sel(server)

    print(response.text)
    print(response)

HANDLE.logout()
