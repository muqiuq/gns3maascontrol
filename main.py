import sys
import time

from maas.client import login
from maas.client.enum import NodeStatus
from maas.client.facade import Client
from maas.client.viscera.machines import Machine

# http://maas.github.io/python-libmaas/

client: Client = login(
    "http://10.0.33.2:5240/MAAS",
    username="sysadm", password="",
)
tmpl = "{0.hostname} {1.name} {1.mac_address}"

machines = client.machines.list()

machine: Machine = client.machines.get(system_id='4ghh3c')

if machine.status != NodeStatus.READY:
    print("Machine ist not ready: ", machine.status_name)
    sys.exit(0)


if machine.status != NodeStatus.ALLOCATED:
    print("Allocating...")
    machine: Machine = client.machines.allocate(hostname=machine.hostname)


machine.deploy()

print("Deploying...")

while machine.status == NodeStatus.DEPLOYING:
    time.sleep(1)
    machine.refresh()

print(machine.status)

print("Done")