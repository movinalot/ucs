"""
set_imc_snmp.py

Purpose:
    Set IMC SNMP Information
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

from imcsdk.imchandle import ImcHandle
import imc_connection as Connection

IMC_HOST = Connection.IMC_HOST
IMC_USER = Connection.IMC_USER
IMC_PASS = Connection.IMC_PASS

def update_snmp():
    """ Update IMC SNMP and Trap Destination """
    handle = ImcHandle(IMC_HOST, IMC_USER, IMC_PASS)
    handle.login()

    imc_snmp = handle.query_dn('sys/svc-ext/snmp-svc')
    imc_snmp.admin_state = 'enabled'
    imc_snmp.community = 'public'
    handle.set_mo(imc_snmp)

    imc_snmp_trap_dest = handle.query_dn('sys/svc-ext/snmp-svc/snmp-trap-1')
    imc_snmp_trap_dest.admin_state = 'enabled'
    imc_snmp_trap_dest.hostname = '10.10.10.10'
    imc_snmp_trap_dest.version = 'v2c'
    handle.set_mo(imc_snmp_trap_dest)

    handle.logout()


if __name__ == '__main__':
    update_snmp()
