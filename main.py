import base64
import os
from pathlib import Path
from typing import List
import typer
from maas.client.enum import NodeStatus
import helper
from maasclientwrapper import MaasClientWrapper

app = typer.Typer()


@app.command()
def checkconfig():
    print(helper.load_config())


@app.command(help="List all hosts with MAAS controller and gns3-cloudinit-backend information")
def listhosts():
    config = helper.load_config()
    client = MaasClientWrapper(config)
    protected_hosts = helper.get_protected_hosts(config)
    comments = helper.get_comments(config)

    gns3_state = helper.get_gns3_state(config)

    machines_unsorted = client.machines()
    machines = {}

    for um in machines_unsorted:
        machines[um.hostname] = um

    machines = dict(sorted(machines.items()))

    for km in machines:
        m = machines[km]
        protected = True if (m.hostname in protected_hosts) else False
        gns3info = ""
        comment = ""
        if m.hostname in gns3_state and m.status == NodeStatus.DEPLOYED:
            gns3info = f"GNS3 Version {gns3_state[m.hostname]['gns3version']} Deployed: {gns3_state[m.hostname]['created']}"
        if m.hostname in comments:
            comment = comments[m.hostname]
        print(f"{m.fqdn} {m.hostname} {m.system_id} {m.status.name} {m.power_state} {gns3info}{' PROTECTED ' if protected else ' '}- {comment}")


@app.command(help="set comment for number of machines", name="comment")
def submit_comment(hosts: List[str], comment: str = typer.Option(...)):
    config = helper.load_config()
    hosts = helper.decode_host_list(hosts)
    data = {}

    for host in hosts:
        data[f'{config["hostprefix"]}{host}'] = comment

    print(helper.update_comments(config, data))


@app.command(help="Download keys from gns3-cloudinit-backend and save it to the desired folder")
def downloadkeys(hosts: List[str], outputfolder: Path = typer.Option(..., exists=False, dir_okay=True, file_okay=False, writable=True, resolve_path=True)):
    config = helper.load_config()
    hosts = helper.decode_host_list(hosts)
    gns3_states = helper.get_gns3_state(config)

    if not outputfolder.exists():
        print("output folder does not exists, creating it.")
        outputfolder.mkdir()

    print(outputfolder)
    downloaded = 0

    for gs in gns3_states:
        hostparts = gs.split("-")
        if hostparts[2] in hosts:
            ovpnb64 = gns3_states[gs]["ovpn"]
            ovpn = base64.b64decode(ovpnb64)
            with open(os.path.join(outputfolder.absolute(), f"{gs}.ovpn"), "wb") as fp:
                fp.write(ovpn)
                downloaded += 1

    print(f"Downloaded {downloaded} keys")


@app.command(help="release list of hosts")
def release(hosts: List[str], commit: bool = False):
    hosts = helper.decode_host_list(hosts)
    config = helper.load_config()
    client = MaasClientWrapper(config)
    protected_hosts = helper.get_protected_hosts(config)

    released_machines = client.release(hosts, protected_hosts, commit)

    print(helper.delete_keys(config, released_machines))


@app.command(help="deploy list of hosts")
def deploy(hosts: List[str], commit: bool = False, comment: str = typer.Option(...)):
    hosts = helper.decode_host_list(hosts)
    config = helper.load_config()
    client = MaasClientWrapper(config)
    protected_hosts = helper.get_protected_hosts(config)
    user_data = helper.get_user_data(config)

    if not user_data.startswith("#cloud-config"):
        print("error: received invalid user-data")
        return

    deployed_machines = client.deploy(hosts, protected_hosts, user_data, commit)

    deployed_machines_with_comment = {}

    for host in deployed_machines:
        deployed_machines_with_comment[host] = comment

    print(helper.update_comments(config, deployed_machines_with_comment))


if __name__ == "__main__":
    app()
