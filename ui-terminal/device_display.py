import os
import subprocess
import sys
import argparse
from time import sleep
from colorama import Fore
import yaml

import requests
from quokka_constants import DISPLAY_WAIT_TIME

parser = argparse.ArgumentParser(description="Device Display")
parser.add_argument('--quokka', default="localhost:5001", help='Hostname/IP and port of the quokka server')

args = parser.parse_args()
quokka = args.quokka


def get_devices():

    try:
        response = requests.get(f"http://{quokka}/devices")
    except requests.ConnectionError as e:
        print(f"!!! connection error: {e}")
        return {}

    if response.status_code != 200:
        print(f"get devices failed: {response.reason}")
        return {}

    return response.json()


def get_compliance_color(device):

    if device["vendor"] not in compliance_table or device["model"] not in compliance_table[device["vendor"]]:
        return Fore.LIGHTBLACK_EX
    elif device["os_version"] != compliance_table[device["vendor"]][device["model"]]:
        return Fore.LIGHTYELLOW_EX
    else:
        return Fore.LIGHTGREEN_EX


def print_devices(devices, previous_devices):

    subprocess.call("clear" if os.name == "posix" else "cls")
    print(
        "\n  __Device_Name___________   ___IP_address___  ______Model_____ "
        + " _Version_ _Avail_ __Rsp_  __Last_Heard___________\n"
    )
    for device in devices.values():

        if not device["availability"]:
            color = Fore.RED
        elif device["name"] in previous_devices and device == previous_devices[device["name"]]:
            color = Fore.GREEN
        else:
            color = Fore.LIGHTGREEN_EX

        compliance_color = get_compliance_color(device)
        version = compliance_color + device["os_version"] + color

        print(
            color
            + f"  {device['hostname'][:24]:<24}"
            + f"  {device['ip_address']:>16}"
            + f"   {device['model'][:16]:<16}"
            + f"   {version:<16}"  # Note: needs extra characters because of colors
            + f"   {str(device['availability']):>5}"
            + f"   {device['response_time']:>5}"
            + f"  {device['last_heard']:>16}"
            + Fore.WHITE
        )

    print()
    for remaining in range(DISPLAY_WAIT_TIME, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(f"  Refresh: {remaining:3d} seconds remaining.")
        sys.stdout.flush()
        sleep(1)

    print("   ... retrieving devices ...")


def main():

    previous_devices = dict()
    while True:
        devices = get_devices()
        print_devices(devices, previous_devices)
        previous_devices = devices


if __name__ == "__main__":

    with open("../server/compliance.yaml", "r") as compliance_yaml:
        compliance_table = yaml.safe_load(compliance_yaml.read())

    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting device-display")
        exit()
