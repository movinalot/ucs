"""
convert_from_ucs_backup.py

Purpose:
    Conver UCS Manager Backup to Python Code
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

from ucsmsdk.utils.convertfrombackup import convert_from_backup

convert_from_backup(
    backup_file="Z:\\Downloads\\ucs-backup.xml",
    output_file="Z:\\Downloads\\ucs_backup.py"
)
