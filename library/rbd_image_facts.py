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
module: rbd_image_facts
short_description: Retrieve facts about an image within rbd command.
version_added: "1.0"
author: "Tomas Rusnak (trusnak@redhat.com)"
description:
  - Retrieve facts about a image image from rbd command.
notes:
  - Facts are placed in the C(rbd) variable.
requirements:
  - "python >= 2.6"
  - "rbd"
options:
  image:
    description:
      - Name or ID of the image
    required: true
  availability_zone:
    description:
      - Ignored. Present for backwards compatability
    required: false
extends_documentation_fragment: ceph
'''

def main():
  module = AnsibleModule(argument_spec={
      "name": {
        "required": True, 
        "default": None,
        "type": "str",
      },
      "id": {
        "required": True, 
        "default": None,
        "type": "str",
      }
  }
  mutually_exclusive=[[ 'name', 'id' ]],
    supports_check_mode=True)

from ansible.module_utils.basic import *
if __name__ == '__main__':
  main()
