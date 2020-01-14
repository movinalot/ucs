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

def add_ucs_bios_policy():
    """ Add UCS BIOS Policy """
    handle = UcsHandle("10.10.10.10", "username", "password")
    handle.login()

    mo_bios_policy = BiosVProfile(
        parent_mo_or_dn='org-root',
        name='test-bios-prof',
        reboot_on_update='yes'
    )
    BiosVfQuietBoot(
        parent_mo_or_dn=mo_bios_policy,
        vp_quiet_boot='disabled'
    )
    BiosVfResumeOnACPowerLoss(
        parent_mo_or_dn=mo_bios_policy,
        vp_resume_on_ac_power_loss='stay-off'
    )
    BiosVfConsoleRedirection(
        parent_mo_or_dn=mo_bios_policy,
        vp_baud_rate='9600',
        vp_console_redirection='com-0',
        vp_terminal_type='pc-ansi'
        )

    handle.add_mo(mo_bios_policy, modify_present=True)
    handle.commit()

if __name__ == '__main__':
    add_ucs_bios_policy()
