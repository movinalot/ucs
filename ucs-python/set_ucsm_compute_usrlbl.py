"""
set_ucsm_compute_usrlbl.py

Purpose:
    add/update a UCS compute resource usrlbl
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

from ucsmsdk.ucshandle import UcsHandle
import connection as Connection

UCS_HOST = Connection.UCS_HOST
UCS_USER = Connection.UCS_USER
UCS_PASS = Connection.UCS_PASS

def update_usrlbl(usrlbl):
    """ Update object usrlbl, ComputeBlade,ComputeRackUnit, LsServer"""
    handle = UcsHandle(UCS_HOST, UCS_USER, UCS_PASS)
    handle.login()

    usrlbl_classes = [
        'computeblade',
        'computerackunit',
        'lsserver'
    ]

    for usrlbl_class in usrlbl_classes:
        compute_mos = handle.query_classid(usrlbl_class)

        for compute_mo in compute_mos:
            if '/blade-' in compute_mo.dn:
                print('blade', compute_mo.dn, 'usrlbl', compute_mo.usr_lbl)
                compute_mo.usr_lbl = usrlbl
            elif '/rackunit-' in compute_mo.dn:
                print('rack', compute_mo.dn, 'usrlbl', compute_mo.usr_lbl)
                compute_mo.usr_lbl = usrlbl
            elif '/ls-' in compute_mo.dn:
                print('service profile', compute_mo.dn, 'usrlbl', compute_mo.usr_lbl)
                compute_mo.usr_lbl = usrlbl

            handle.add_mo(compute_mo, modify_present=True)

    handle.commit()

if __name__ == '__main__':
    update_usrlbl('')
