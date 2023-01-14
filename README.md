# GNS3 MAAS Control CLI tool

gns3maascontrol was developed to facilitate the deployment of node in the [TBZ Cloud GNS3 environment](https://gitlab.com/ch-tbz-it/Stud/allgemein/tbzcloud-gns3).

## Get started - Windows

### Requirements
 - python3.9 or newer
 - git
 - Windows 10 or newer

**Powershell:**
```shell
$ git clone https://github.com/muqiuq/gns3maascontrol
$ cd gns3maascontrol
$ python -m venv venv
$ .\venv\Scripts\Activate.ps1
$ pip3 install -r requirements.txt
```
Before starting `main.py` copy `config.yaml` into gns3maascontrol directory. 

```
$ python main.py
```


## Usage

### Requirements
 - configuration file (`config.yaml`) in the same directory. it contains the relevant backend URLs and credentials.
 - Layer 3 connectivity to control server (currently implemented with wireguard)

### list hosts
To list all the hosts use `gns3maascontrol listhosts`

example: 
```shell
$ gns3maascontrol listhosts
Cloud-HF-26.maas Cloud-HF-26 abc123 DEPLOYED PowerState.ON  PROTECTED - Reserved
Cloud-HF-27.maas Cloud-HF-27 abc323 DEPLOYED PowerState.ON GNS3 Version 2.2.35.1 Deployed: 2022-11-30 11:01:02 - Class2b
Cloud-HF-28.maas Cloud-HF-28 abc372 DEPLOYED PowerState.ON GNS3 Version 2.2.35.1 Deployed: 2022-11-30 11:00:01 - Class2b
```

each line contains:
```
<-FQDN        -> <-HOST    > < ID > < STATE> <PowerState > <Current GNS3 Version and update date             >   <comment>
Cloud-HF-28.maas Cloud-HF-28 abc372 DEPLOYED PowerState.ON GNS3 Version 2.2.35.1 Deployed: 2022-11-30 11:00:01 - Class2b
```

### deploy hosts
to deploy a single or multiple host the selected hosts must be ready or allocated

example: 
```shell
$ gns3maascontrol deploy 1-4,7,9 --comment "Class3b, Prof. Duncan, till Sept 23"
Dry run. No hosts will be released.
Skipped: 0
Deployed: 6
Number of machines: 20
Updated: 6
```

to actually commit the requested changes and deploy the hosts, you need to add `--commit` as option

### relase hosts
```shell
$ gns3maascontrol deploy 20-24
Dry run. No hosts will be released.
Releasing Cloud-HF-20
Releasing Cloud-HF-21
Releasing Cloud-HF-22
Releasing Cloud-HF-23
Releasing Cloud-HF-24
Skipped: 0
Released: 1
Number of machines: 19
Deleted: 0
```

to actually commit the requested changes and release the hosts, you need to add `--commit` as option

### download openvpn keys to folder
to download the openvpn of deployed and installed hosts

output folder will be created, if it does not exists

```shell
$ gns3maascontrol downloadkeys 30-40 --outputfolder out 
output folder does not exists, creating it.
Downloaded 11 keys
```

### comment
while the comment is required when deploying hosts, the comments can be updated manually

```shell
$ gns3maascontrol comment 44 --comment "Not used" 
Updated: 1
```

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a> and [GNU GENERAL PUBLIC LICENSE version 3](https://www.gnu.org/licenses/gpl-3.0.en.html). If there are any contradictions between the two licenses, the Attribution-NonCommercial-ShareAlike 4.0 International license governs. 