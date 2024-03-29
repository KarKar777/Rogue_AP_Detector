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
        res = subprocess.check_output("iw dev wlan0 link", shell=True)
        # out = res.decode("utf-8")
        res = str(res.decode())
        list_of_parameters = ["SSID", "signal", "rx bitrate", "tx bitrate"]
        list_of_names = ["ssid", "signal", "receive_rate", "transmit_rate"]
        res_json["bssid"] = res[res.find("Connected to ")+12:res.find("(")].strip()
        out = res
        for i in range(len(list_of_parameters)):
            out = out[out.find(list_of_parameters[i]):]
            res_json[list_of_names[i]] = out[out.find(":") + 2:out.find("\n")].rstrip()
        
        res_json["transmit_rate"] = res_json["transmit_rate"][:res_json["transmit_rate"].find("MBit/s")-1]
        res_json["receive_rate"] = res_json["receive_rate"][:res_json["receive_rate"].find("MBit/s")-1]
        res_json["signal"] = res_json["signal"][1:res_json["signal"].find("dBm")-1]


        return res_json
    except Exception as err:
       return 0

def compare_wifi_params(old_params: dict, cur_params: dict):
    try:
        signal_change = False
        static_param_change = False
        for i in list(cur_params.keys()):
            if i == "signal":
                s1 = int(cur_params[i])
                s2 = int(old_params[i])
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
