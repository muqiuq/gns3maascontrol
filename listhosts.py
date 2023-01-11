import sys
import time

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
tmpl = "{0} {1} {2} {3} {4}"

machines = client.machines.list()

for m in machines:
    print(tmpl.format(m.fqdn, m.hostname, m.system_id, m.status.name, m.power_state))