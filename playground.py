import sys
import time

import requests
from maas.client import login
from maas.client.enum import NodeStatus
from maas.client.facade import Client
from maas.client.viscera.machines import Machine

# http://maas.github.io/python-libmaas/
import config

client: Client = login(
    config.host,
    username=config.username, password=config.password,
)
tmpl = "{0.hostname} {1.name} {1.mac_address}"

machines = client.machines.list()

machine: Machine = client.machines.get(system_id='4ghh3c')



with open('user-data', 'r') as file:
    userdata = file.read()


if machine.status != NodeStatus.READY:
    print("Machine ist not ready: ", machine.status_name)
    sys.exit(0)


if machine.status != NodeStatus.ALLOCATED:
    print("Allocating...")
    machine: Machine = client.machines.allocate(hostname=machine.hostname)


machine.deploy(user_data=userdata)

print("Deploying...")

while machine.status == NodeStatus.DEPLOYING:
    time.sleep(1)
    machine.refresh()

print(machine.status)

code = 0

print("Waiting for GNS3 setup...")

while code != 200:
    r = requests.get('http://10.1.40.33/gns3cloudinit/keys/Cloud-HF-27.json')
    code = r.status_code
    time.sleep(1)


print("Done")