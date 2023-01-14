import json
from typing import List

import requests
import yaml
from maas.client import login
from maas.client.facade import Client


def load_config(config_filepath: str = "config.yaml"):
    with open(config_filepath, mode="rt", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config


def get_protected_hosts(config):
    res = requests.get(config["gns3cloudinithelper"]["url"] + "/protected-hosts")
    return res.content.decode("utf-8").split("\n")


def get_user_data(config) -> str:
    res = requests.get(config["gns3cloudinithelper"]["url"] + "/user-data")
    return res.content.decode("utf-8")


def get_gns3_state(config):
    res = requests.get(config["gns3cloudinithelper"]["url"] + "/list.php?token=vrb2-t7vd-bw8x")
    return json.loads(res.content.decode("utf-8"))


def get_comments(config):
    res = requests.get(config["gns3cloudinithelper"]["url"] + "/comments.json")
    return json.loads(res.content.decode("utf-8"))


def update_comments(config, comments) -> str:
    req_data = {"submit":"comments", "data": comments}
    res = requests.post(config["gns3cloudinithelper"]["url"] + "/comment.php", json=req_data)
    return res.content.decode("utf-8")


def delete_keys(config, hosts) -> str:
    req_data = {"submit": "delete", "data": hosts}
    res = requests.post(config["gns3cloudinithelper"]["url"] + "/delete.php", json=req_data)
    return res.content.decode("utf-8")


def decode_host_list(hosts: List[str]) -> List[str]:
    prelist = []
    for host in hosts:
        if "," in host:
            hostparts = host.split(",")
            for hostp in hostparts:
                prelist.append(hostp)
        else:
            prelist.append(host)

    outlist = []
    for host in prelist:
        if host.isdigit():
            outlist.append(host)
        elif "-" in host:
            hostparts = host.split("-")
            if len(hostparts) == 2:
                for i in range(int(hostparts[0]), int(hostparts[1])+1):
                    outlist.append(str(i))
            else:
                raise ValueError("invalid syntax in host list. a '-' can only be use once per element")
    return outlist