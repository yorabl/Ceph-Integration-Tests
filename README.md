# ceph-osp-acceptance testsuite based on Ansible modules

## Requirements
- python-shade library
- openstack-python library
- ansible
- deployed OpenStack with TripleO

## Inventory

Edit hosts file according your openstack and ceph setup, or you can use one from infrared deployment.

$ cat hosts
[undercloud]
undercloud-0:5000

[ceph]
ceph-0:5001

## Authentication

Auth directive is used for all commands in ansible core os modules. The wrapper - auth.yml is used
to do all magic needed to parse overcloudrc and pass it as yaml parameters.

$ cat overcloudrc
export OS_NO_CACHE=True
export OS_CLOUDNAME=overcloud
export OS_AUTH_URL=http://10.0.0.106:5000/v2.0
export NOVA_VERSION=1.1
export COMPUTE_API_VERSION=1.1
export OS_USERNAME=admin
export no_proxy=,10.0.0.106,192.168.24.11
export OS_PASSWORD=xxxxxxxx
export PYTHONWARNINGS="ignore:Certificate has no, ignore:A true SSLContext object is not available"
export OS_TENANT_NAME=admin

### Run tests

./run.sh
or
ansible-playbook -i hosts test_volume_size.yml

## Todo
1. add more RBD commands and parsers
2. split RBD commands to rbd_*_fetch (fetch infromation from cluster) and rbd_* (set cluster parameters)



