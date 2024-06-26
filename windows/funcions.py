import subprocess
import os
import time


def get_wifi_params_to_str():
    d = get_wifi_params()
    s = ""
    for i in d.keys():
        s += i + " : " + d[i] + " \n"
    return s


def get_visible_wifi():
    try:

        os.system("chcp 65001 > nul")  # for normal output of ru symbols in terminal
        res_json = {}

        res = subprocess.check_output("netsh wlan show networks", shell=True)
        out = res.decode("utf-8")
        wifi_net_count = int(out[out.rfind("SSID") + 5])

        # get ssid, network_type, auth, encryption
        for i in range(1, wifi_net_count + 1):
            cur_wifi_dict = {}
            if i == wifi_net_count:
                cur_wifi_info = out[out.find(f"SSID {i}"):]
            else:
                cur_wifi_info = out[out.find(f"SSID {i}"):out.find(f"SSID {i + 1}")]
            cur_wifi_dict["ssid"] = cur_wifi_info[cur_wifi_info.find(":") + 2:cur_wifi_info.find("\r")].rstrip()
            cur_wifi_info = cur_wifi_info[cur_wifi_info.find('\n') + 1:]

            if "Network type".lower() in cur_wifi_info.lower():
                cur_wifi_dict["network_type"] = cur_wifi_info[
                                                cur_wifi_info.find(":") + 2:cur_wifi_info.find("\r")].rstrip()

            cur_wifi_info = cur_wifi_info[cur_wifi_info.find('\n') + 1:]
            if "Authentication".lower() in cur_wifi_info.lower():
                cur_wifi_dict["auth"] = cur_wifi_info[cur_wifi_info.find(":") + 2:cur_wifi_info.find("\r")].rstrip()

            cur_wifi_info = cur_wifi_info[cur_wifi_info.find('\n') + 1:]
            if "Encryption".lower() in cur_wifi_info.lower():
                cur_wifi_dict["encryption"] = cur_wifi_info[
                                              cur_wifi_info.find(":") + 2:cur_wifi_info.find("\r")].rstrip()

            res_json[f"ssid_{i}"] = cur_wifi_dict
        return res_json
    except subprocess.CalledProcessError:
        print("Error in wifi module")
        return 0


def get_wifi_params():
    try:
        res_json = {}
        os.system("chcp 65001 > nul")  # for normal output of ru symbols in terminal
        res = subprocess.check_output("ipconfig /all", shell=True)
        # out = res.decode("utf-8")
        out = str(res)[2:-1]
        out = out[out.find("Wireless LAN adapter"):out.rfind("NetBIOS over Tcpip")]

        out = out[out.find("DNS Servers"):out.find("\n")]
        router_ip = out[out.find(":"):out.find("\n")]
        router_ip = router_ip[router_ip.find(": ") + 2:router_ip.rfind("\\r")]
        router_ip = router_ip[router_ip.rfind(" ") + 1:]

        """os.system("chcp 65001 > nul")  # for normal output of ru symbols in terminal
        res = subprocess.check_output("arp -a", shell=True)
        out = res.decode("utf-8")

        router_mac = out[out.find(router_ip + " "):]
        router_mac = router_mac[11 + len(router_ip):router_mac.find("\n")]
        router_mac = router_mac[:router_mac.find(" ")]

        res_json["router_mac"] = router_mac"""
        res_json["router_ip"] = router_ip

        os.system("chcp 65001 > nul")  # for normal output of ru symbols in terminal
        res = subprocess.check_output("netsh wlan show interfaces", shell=True)
        out = res.decode("utf-8")

        list_of_parameters = ["Interface type", "State", "SSID", "BSSID", "Authentication", "Cipher", "Connection mode",
                              "Band", "Channel", "Receive rate (Mbps)", "Transmit rate (Mbps)", "Signal"]
        list_of_names = ["interface_type", "state", "ssid", "bssid", "auth", "cipher", "connection_mode",
                         "band", "channel", "receive_rate", "transmit_rate", "signal"]
        for i in range(len(list_of_parameters)):
            out = out[out.find(list_of_parameters[i]):]
            res_json[list_of_names[i]] = out[out.find(":") + 2:out.find("\n")].rstrip()

        return res_json
    except Exception as err:
        print(err)
        return 0


def compare_wifi_params(old_params: dict, cur_params: dict):
    try:
        signal_change = False
        static_param_change = False
        for i in list(cur_params.keys()):
            if i == "signal":
                s1 = int(cur_params[i][:-1])
                s2 = int(old_params[i][:-1])
                if abs(s2 - s1) > 15:
                    signal_change = True
            elif i == "receive_rate" or i == "transmit_rate":
                pass
            else:
                if old_params[i] != cur_params[i]:
                    static_param_change = True

        if signal_change and static_param_change:
            return 3
        elif signal_change:
            return 1
        elif static_param_change:
            return 2
        else:
            return 0
    except Exception as err:
        print(err)
        return 4
