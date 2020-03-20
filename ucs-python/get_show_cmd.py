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

def process_command(remote_connection, command, sleep_time=2, recv_buffer=10000):
    '''Process Command on Cisco UCS CLI'''

    #print(command, sleep_time)
    remote_connection.send(command+'\n')
    time.sleep(sleep_time)

    # Clear the buffer on the screen
    remote_output = remote_connection.recv(recv_buffer)

    return remote_output

if __name__ == '__main__':

    FILENAME = os.path.join(sys.path[0], sys.argv[1])

    try:
        with open(FILENAME, 'r') as file:
            if FILENAME.endswith('.json'):
                COMMANDS = json.load(file)
            elif FILENAME.endswith('.yml'):
                COMMANDS = yaml.load(file, Loader=yaml.FullLoader)
            else:
                print(
                    'Unsupported file extension for command file: %s'
                    , FILENAME
                    )

    except IOError as io_error:
        sys.exit(io_error)

    REMOTE_CONNECTION_PRE = paramiko.SSHClient()

    REMOTE_CONNECTION_PRE.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    REMOTE_CONNECTION_PRE.connect(
        COMMANDS['connection']['hostname'],
        username=COMMANDS['connection']['username'],
        password=COMMANDS['connection']['password'],
        look_for_keys=False,
        allow_agent=False
        )

    print("SSH connection established to " + COMMANDS['connection']['hostname'])

    REMOTE_CONNECTION = REMOTE_CONNECTION_PRE.invoke_shell()
    print("Interactive SSH session established")

    for remote_commands in COMMANDS['commands']:
        output = process_command(REMOTE_CONNECTION, **remote_commands)
        print(output.decode('utf-8'))
