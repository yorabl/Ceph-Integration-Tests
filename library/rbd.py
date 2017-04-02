#!/usr/bin/python
# -*- coding: utf-8 -*-
DOCUMENTATION = '''
---
module: rbd
short_description: Manages ceph RBD command
description:
  - Manages ceph rbd command line tools
  version_added: "0.0.1"
options:
  action:
    description:
      - manage rbd images
    required: false
    default: none
  snap:
    description:
      - manage rbd snapshots
    required: false
    default: none
'''

import sys
import json
import os
from ansible.module_utils.basic import AnsibleModule

def rbd(m, params):
  rc, out, err = m.run_command(rbd_action_wrapper(params))
  if rc:
    return (True, False, dict(msg="failed: '%s'" % (err), stdout=out, stderr=err))
  if out:
    if params['action']:
      # return image object_size in GB
      data = json.loads(out)
      data['object_size'] = str(int(data['object_size'])/(1024**2))
      return False, True, dict(image=data)
    if params['snap']:
      return False, True, dict(snapshot=json.loads(out))
  return False, True, dict(response="success")

def rbd_action_wrapper(params):
  if params['action'] == "create":
    return "rbd create -s " + str(params['size']) + " " + params['pool'] + "/" + params['image']

  if params['action'] == "rm":
    return "rbd rm " + params['pool'] + "/" + params['image']

  if params['snap'] == "list":
    return "rbd snap list " + params['pool'] + "/" + params['image'] + " --format json"

  if params['snap'] == "create":
    return "rbd snap create " + params['pool'] + "/" + params['image'] + "@" + params['snap_name']

  if params['snap'] == "rm":
    return "rbd snap rm " + params['pool'] + "/" + params['image'] + "@" + params['snap_name']

  if params['snap'] == "rollback":
    return "rbd snap rollback" + params['pool'] + "/" + params['image'] + "@" + params['snap_name']

  if params['snap'] == "purge":
    return "rbd snap purge" + params['pool'] + "/" + params['image']

  if params['action'] == "clone":
    return "rbd clone " + params['pool'] + "/" + params['image'] + "@" + params['snap_name'] \
      + ' ' + params['pool'] + "/" + params['image_clone']

  else:
    return "rbd info " + params['pool'] + "/" + params['image'] + " --format json"  

def main():

  module = AnsibleModule(argument_spec={
      "action": {
        "required": False, 
        "choices": ['rm', 'info', 'create', 'clone'],
        "type": "str",
      },
      "pool": {
        "required": False,
        "default": "rbd",
        "type": "str"
      },
      "image": {
        "required": True,
        "default": None,
        "type": "str"
      },
      "image_clone": {
        "required": False,
        "default": None,
        "type": "str"
      },
      "size": {
        "required": False,
        "default": 1,
        "type": "int"
      },
      "snap": {
        "required": False,
        "choices": ['rm', 'list', 'create', 'rollback', 'purge'],
        "type": "str"
      },
      "snap_name": {
        "required": False,
        "default": None,
        "type": "str" 
      },
    },
    mutually_exclusive=[[ 'action', 'snap' ]],
    supports_check_mode=True)

  if 'action' in module.params and module.params['action']:
    #if p['rbd']:
    is_error, has_changed, result = rbd(module, module.params)
  if 'snap' in module.params and module.params['snap']:
    is_error, has_changed, result = rbd(module, module.params)

  if not is_error:
    module.exit_json(changed=has_changed, **result)
  else:
    module.fail_json(msg="Error", meta=result)

if __name__ == "__main__":
  main()
