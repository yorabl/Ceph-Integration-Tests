#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2017 Tomas Rusnak <trusnak@redhat.com>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: rbd_image
short_description: Manages ceph RBD images
description:
  - Manages ceph rbd image command line tool
  version_added: "1.0"
options:
  status:
    description:
      - manage rbd images
    required: True
    default: none
'''

import sys
import json
import os
from ansible.module_utils.basic import AnsibleModule

def cmd(m, params):
  rc, out, err = m.run_command(cmd_action_wrapper(params))
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

def cmd_action_wrapper(params):
  if params['state'] == "present":
    return "rbd create -s " + str(params['size']) + " " + params['pool'] + "/" + params['image']
  else:
    return "rbd info " + params['pool'] + "/" + params['image'] + " --format json"  


def main():

  module = AnsibleModule(argument_spec={
      "state": {
        "required": True, 
        "choices": ['present', 'absent'],
        "type": "str",
      },
      "name": {
        "required": True, 
        "default": None,
        "type": "str",
      },
      "size": {§
        "required": False, 
        "default": None,
        "type": "str",
      },
      "pool": {
        "required": False,
        "default": None,
        "type": "str"
      },
      "clone": {
        "required": False,
        "default": None,
        "type": "str"
      },
    },
    supports_check_mode=True)

  if 'action' in module.params and module.params['action']:
    #if p['rbd']:
    is_error, has_changed, result = cmd(module, module.params)
  if 'snap' in module.params and module.params['snap']:
    is_error, has_changed, result = cmd(module, module.params)

  if not is_error:
    module.exit_json(changed=has_changed, **result)
  else:
    module.fail_json(msg="Error", meta=result)

if __name__ == "__main__":
  main()
