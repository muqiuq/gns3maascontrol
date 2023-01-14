from typing import List

from maas.client import login
from maas.client.enum import NodeStatus
from maas.client.facade import Client
from maas.client.viscera.machines import Machine


class MaasClientWrapper:

    def __init__(self, config):
        self.url = config["maas"]["url"]
        self.username = config["maas"]["username"]
        self.password = config["maas"]["password"]

    def _getclient(self) -> Client:
        client: Client = login(
            self.url,
            username=self.username, password=self.password,
        )
        return client

    def release(self, hosts: List[str], protected_hosts: List[str], commit: bool = False):
        client = self._getclient()

        machines = client.machines.list()

        released = 0
        skipped = 0
        total = 0

        print("This is not a drill. Host will be released." if commit else "Dry run. No hosts will be released.")

        for m in machines:
            protected = True if (m.hostname in protected_hosts) else False
            total += 1
            hostparts = m.hostname.split("-")
            if hostparts[2] in hosts:
                if protected:
                    print(f"Host {m.hostname} is protected cannot release")
                    skipped += 1
                elif m.status == NodeStatus.DEPLOYED:
                    print(f"Releasing {m.hostname}")
                    if commit:
                        m.release(quick_erase=True, erase=True)
                    released += 1
                else:
                    print(f"host {m.hostname} is not deployed. Currently in status: {m.status}")

        print(f"Skipped: {skipped}")
        print(f"Released: {released}")
        print(f"Number of machines: {total}")

    @staticmethod
    def _deploy_machine(client: Client, m: Machine, user_data: str, commit: bool = False):
        if not (m.status == NodeStatus.READY or m.status == NodeStatus.ALLOCATED):
            return False

        if m.status != NodeStatus.ALLOCATED:
            m: Machine = client.machines.allocate(hostname=m.hostname)

        if commit:
            m.deploy(user_data=user_data)

        return True

    def deploy(self, hosts: List[str], protected_hosts: List[str], user_data: str, commit: bool = False):
        client = self._getclient()

        machines = client.machines.list()

        deployed = 0
        skipped = 0
        total = 0

        print("This is not a drill. Host will be released." if commit else "Dry run. No hosts will be released.")

        for m in machines:
            protected = True if (m.hostname in protected_hosts) else False
            total += 1
            hostparts = m.hostname.split("-")
            if hostparts[2] in hosts:
                if protected:
                    print(f"Host {m.hostname} is protected cannot release => Skipping")
                    skipped += 1
                elif m.status == NodeStatus.ALLOCATED:
                    if self._deploy_machine(client, m, user_data, commit):
                        print("Deployed {0}".format(m.hostname))
                        deployed += 1
                    else:
                        print("Deploy error {0}".format(m.hostname))
                else:
                    print(f"Cannot deploy {m.hostname}. Host not ready. Release first.")

        print(f"Skipped: {skipped}")
        print(f"Deployed: {deployed}")
        print(f"Number of machines: {total}")

    def machines(self):
        client = self._getclient()

        machines = client.machines.list()

        return machines

