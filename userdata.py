from typing import Dict, List


class UserData:

    def __init__(self, user_data: str, host_select_patterns: List):
        self.host_select_patterns = host_select_patterns
        self.user_data = user_data

    def get_user_data_for_ip(self, ip):
        for hsp in self.host_select_patterns:
            if hsp["pattern"] in ip:
                edit_user_data = self.user_data
                edit_user_data = edit_user_data.replace("[NUM]", hsp["NUM"]).replace("[HOST]", hsp["HOST"])
                return edit_user_data
        raise Exception("found no host config for ip")

