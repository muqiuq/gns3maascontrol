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
tmpl = "{0} {1} {2} {3}"

machines = client.machines.list()

excluded_hosts = ["Cloud-HF-26"]
included_host_nums = []
included_hosts = []

for included_host_num in included_host_nums:
    included_hosts.append("Cloud-HF-" + str(included_host_num))

released = 0
skipped = 0
total = 0


for m in machines:
    print(tmpl.format(m.fqdn, m.hostname, m.system_id, m.status.name))
    total += 1
    if m.hostname in excluded_hosts:
        print("==> Host excluded (Skipping)")
        skipped += 1
        continue
    if len(included_hosts) > 0 and m.hostname not in included_hosts:
        print("==> Host not included (Skipping)")
        skipped += 1
        continue
    if m.status == NodeStatus.DEPLOYED:
        # m.release(quick_erase=True, erase=True)
        print("==> Releasing (Erasing)")
        released += 1


print(f"Skipped: {skipped}")
print(f"Released: {released}")
print(f"Total: {total}")