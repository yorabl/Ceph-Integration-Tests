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

import sys
import json
import os
import shlex
from ansible.module_utils.basic import AnsibleModule

# -*- coding: utf-8 -*-
DOCUMENTATION = '''
---
module: ceph_cmd
short_description: Manages ceph cmd tools
description:
  - Manages ceph command line tools
  version_added: "0.0.1"
options:
  state:
    description:
      - get ceph cluster status
    required: false
    default: check
  rbd:
    description:
      - manage rbd images
    required: false
    default: info
'''


def state(m, data):
    cmd = "ceph -s --format json"
    rc, out, err = m.run_command(cmd)

    if rc:
        return True, False, dict(msg="'%s' failed: %s" % (cmd, err), stdout=out, stderr=err)
    else:
        return False, True, dict(status=json.loads(out))


def main():
    fields = {
      "state": {
        "default": "check",
        "choices": ["check"],
        "type": "str"
      },
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)
    try:
        if 'state' in module.params and module.params['state']:
            is_error, has_changed, result = state(module, module.params)

        if not is_error:
            module.exit_json(changed=has_changed, **result)
        else:
            module.fail_json(changed=has_changed, msg="Error", meta=result)
    except Exception as e:
        module.fail_json(msg="Module error", meta=e)

if __name__ == "__main__":
    main()
