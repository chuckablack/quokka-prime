import os
import subprocess
import sys
from time import sleep
from colorama import Fore
import argparse
import requests
from quokka_constants import DISPLAY_WAIT_TIME

MAX_HOST_SLA_RESPONSE_TIME = 0.2


def get_host_status(hostname):

    response = requests.get(f"http://127.0.0.1:5001/host/status?hostname={hostname}")
    if response.status_code != 200:
        print(f"get hosts failed: {response.reason}")
        return {}

    return response.json()


def print_host_status(host, host_status, previous_host_status):

    previous_times = set()
    for previous_host_status_record in previous_host_status:
        previous_times.add(previous_host_status_record["time"])

    subprocess.call("clear" if os.name == "posix" else "cls")
    print(f"\n Host Status: {host['hostname']}\n")
    print("  __Time_________________  ___Avail___  ___RspTime___\n")
    for host_status_record in host_status:

        if not host_status_record["availability"]:
            color = Fore.RED
        elif float(host_status_record["response_time"]) > MAX_HOST_SLA_RESPONSE_TIME:
            color = Fore.LIGHTCYAN_EX
        elif host_status_record["time"] in previous_times:
            color = Fore.GREEN
        else:
            color = Fore.LIGHTGREEN_EX

        print(
            color +
            f"  {host_status_record['time']:<16}"
            + f"   {str(host_status_record['availability']):>6}  "
            + f"   {float(host_status_record['response_time']):>9.4f}"
            + Fore.WHITE
        )

    print()
    for remaining in range(DISPLAY_WAIT_TIME, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(f"  Refresh: {remaining:3d} seconds remaining.")
        sys.stdout.flush()
        sleep(1)

    print("   ... retrieving hosts ...")


def main():

    parser = argparse.ArgumentParser(description="Host Status display")
    parser.add_argument(
        "-H",
        "--hostname",
        required=True,
        help="Name of the host for getting status",
    )
    args = parser.parse_args()
    hostname = args.hostname

    previous_host_status = list()
    while True:
        host_status = get_host_status(hostname)
        if "status" in host_status and "host" in host_status:
            print_host_status(host_status["host"], host_status["status"], previous_host_status)
            previous_host_status = host_status["status"]
        else:
            print(f"Error getting host status for {hostname}!")
            sleep(DISPLAY_WAIT_TIME)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting host-status-display")
        exit()
