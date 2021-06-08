import os
import subprocess
import sys
from time import sleep
from colorama import Fore
import argparse
import requests
from quokka_constants import DISPLAY_WAIT_TIME


def get_device_status(name):

    response = requests.get(f"http://127.0.0.1:5001/device/status?name={name}")
    if response.status_code != 200:
        print(f"get devices failed: {response.reason}")
        return {}

    return response.json()


def print_device_status(device, device_status, previous_device_status):

    previous_times = set()
    for previous_device_status_record in previous_device_status:
        previous_times.add(previous_device_status_record["time"])

    subprocess.call("clear" if os.name == "posix" else "cls")
    print(f"\n Device Status: {device['name']}\n")
    print("  __Time_________________  ___Avail___  ___RspTime___\n")
    for device_status_record in device_status:

        if not device_status_record["availability"]:
            color = Fore.RED
        elif float(device_status_record["response_time"]) > device["sla_response_time"]:
            color = Fore.LIGHTCYAN_EX
        elif device_status_record["time"] in previous_times:
            color = Fore.GREEN
        else:
            color = Fore.LIGHTGREEN_EX

        print(
            color +
            f"  {device_status_record['time']:<16}"
            + f"   {str(device_status_record['availability']):>6}  "
            + f"   {float(device_status_record['response_time']):>9.4f}"
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

    parser = argparse.ArgumentParser(description="Device Status display")
    parser.add_argument(
        "-H",
        "--name",
        required=True,
        help="Name of the device for getting status",
    )
    args = parser.parse_args()
    name = args.name

    previous_device_status = list()
    while True:
        device_status = get_device_status(name)
        if "status" in device_status and "device" in device_status:
            print_device_status(device_status["device"], device_status["status"], previous_device_status)
            previous_device_status = device_status["status"]
        else:
            print(f"Error getting device status for {name}!")
            sleep(DISPLAY_WAIT_TIME)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting device-status-display")
        exit()
