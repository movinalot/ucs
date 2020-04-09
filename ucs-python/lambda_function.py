"""
lambda_function.py

Purpose:
    Generic UCS Manager AWS Lambda Function
    UCS Python SDK is added in a Layer

Author:
    John McDonough (jomcdono@cisco.com) github: (@movinalot)
    Cisco Systems, Inc.

Example BODY sent to AWS API Gateway
    Connects to specified UCSM
    Creates an Organization

    {
        "auth": {
            "hostname": "ucsm.company.com",
            "username": "admin",
            "password": "password"
        },
        "action": {
            "method": "configure",
            "objects": [
            {
                    "module": "ucsmsdk.mometa.org.OrgOrg",
                    "class": "OrgOrg",
                    "properties":{
                        "parent_mo_or_dn": "org-root",
                        "name": "Org01"
                    },
                    "message": "created organization Org01"
                }
            ]
        }
    }
Example BODY sent to AWS API Gateway
    Connects to specified UCSM
    Queries the Class ID computeRackUnit
    {
        "auth": {
            "hostname": "ucsm.company.com",
            "username": "admin",
            "password": "password"
        },
        "action": {
            "method": "query_classid",
            "class_id": "computeRackUnit"
        }
    }
"""
# pylint: disable=invalid-name, global-statement, unused-argument

from importlib import import_module
import copy
from ucsmsdk.ucshandle import UcsHandle
# ucsmsdk is a Layer associated with the lambda function

RETURN_DICT = dict()
MO_DICT_LIST = list()
OBJECT_COUNT = 0

def make_mo_dict(mo):
    """ Turn response objects into JSON """

    obj_dict = dict()
    for mo_property in mo.prop_map.values():
        obj_dict[mo_property] = getattr(mo, mo_property)

    return obj_dict

def query_classid(handle, class_id):
    """ Query UCS Class IDs """

    query_response = dict()
    mos = handle.query_classid(class_id)

    for mo in mos:
        MO_DICT_LIST.append(make_mo_dict(mo))

    query_response = {"object_count": len(mos), class_id: MO_DICT_LIST}

    return query_response

def traverse(handle, managed_object, mo=''):
    """ Create/Update Object and children """

    global OBJECT_COUNT

    mo_module = import_module(managed_object['module'])
    mo_class = getattr(mo_module, managed_object['class'])

    if 'parent_mo_or_dn' not in managed_object['properties']:
        managed_object['properties']['parent_mo_or_dn'] = mo

    mo = mo_class(**managed_object['properties'])

    handle.add_mo(mo, modify_present=True)

    OBJECT_COUNT += 1

    if 'children' in managed_object:
        for child in managed_object['children']:
            traverse(handle, child, mo)

def configure_mos(handle, config):
    """ Configure managed objects from JSON """

    for managed_object in config['objects']:
        traverse(handle, managed_object)
        handle.commit()

    return {"object_count": OBJECT_COUNT}

def process_request(event):
    """ Process the UCS Request """

    handle = UcsHandle(
        event['auth']['hostname'],
        event['auth']['username'],
        event['auth']['password'])
    handle.login()

    if event['action']['method'] == 'query_classid':
        RETURN_DICT['response'] = query_classid(handle, event['action']['class_id'])
    elif event['action']['method'] == 'configure':
        RETURN_DICT['response'] = configure_mos(handle, event['action'])

    handle.logout()

def lambda_handler(event, context):
    """ Entry point ot process the Request """
    print(event)

    if 'auth' in event and 'action' in event:

        RETURN_DICT['request'] = copy.deepcopy(event)

        process_request(event)

        if 'password' in RETURN_DICT['request']['auth']:
            RETURN_DICT['request']['auth']['password'] = (
                '*' * len(RETURN_DICT['request']['auth']['password'])
            )

        status_code = 200
    else:
        RETURN_DICT['error'] = "malformed request"
        status_code = 400

    print(RETURN_DICT)

    return {
        'statusCode': status_code,
        'body': RETURN_DICT
    }
