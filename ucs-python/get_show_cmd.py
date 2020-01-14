"""
get_show_cmd.py

Purpose:
    Access UCSM CLI
Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.
"""

import time
import json
import os
import sys
import paramiko
import yaml

def process_command(remote_conn, command, sleep_time=2, recv_buffer=10000):
    '''Process Command on Cisco UCS CLI'''

    #print(command, sleep_time)
    remote_conn.send(command+'\n')
    time.sleep(sleep_time)

    # Clear the buffer on the screen
    output = remote_conn.recv(recv_buffer)

    return output

if __name__ == '__main__':

    FILENAME = os.path.join(sys.path[0], sys.argv[1])

    try:
        with open(FILENAME, 'r') as file:
            if FILENAME.endswith('.json'):
                commands = json.load(file)
            elif FILENAME.endswith('.yml'):
                commands = yaml.load(file, Loader=yaml.FullLoader)
            else:
                print(
                    'Unsupported file extension for command file: %s'
                    , FILENAME
                    )

    except IOError as io_error:
        sys.exit(io_error)

    remote_conn_pre = paramiko.SSHClient()

    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(
        commands['connection']['hostname'],
        username=commands['connection']['username'],
        password=commands['connection']['password'],
        look_for_keys=False,
        allow_agent=False
        )

    print("SSH connection established to " + commands['connection']['hostname'])

    remote_conn = remote_conn_pre.invoke_shell()
    print("Interactive SSH session established")

    for command in commands['commands']:
        output = process_command(remote_conn, **command)
        print(output.decode('utf-8'))
