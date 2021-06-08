import os
import subprocess
import sys
from time import sleep
from colorama import Fore
import argparse
import requests
from quokka_constants import DISPLAY_WAIT_TIME


def get_service_status(name):

    response = requests.get(f"http://127.0.0.1:5001/service/status?name={name}")
    if response.status_code != 200:
        print(f"get services failed: {response.reason}")
        return {}

    return response.json()


def print_service_status(service, service_status, previous_service_status):

    previous_times = set()
    for previous_service_status_record in previous_service_status:
        previous_times.add(previous_service_status_record["time"])

    subprocess.call("clear" if os.name == "posix" else "cls")
    print(f"\n Service Status: {service['name']}\n")
    print("  __Time_________________  ___Avail___  ___RspTime___\n")
    for service_status_record in service_status:

        if not service_status_record["availability"]:
            color = Fore.RED
        elif float(service_status_record["response_time"]) > service["sla_response_time"]:
            color = Fore.LIGHTCYAN_EX
        elif service_status_record["time"] in previous_times:
            color = Fore.GREEN
        else:
            color = Fore.LIGHTGREEN_EX

        print(
            color +
            f"  {service_status_record['time']:<16}"
            + f"   {str(service_status_record['availability']):>6}  "
            + f"   {float(service_status_record['response_time']):>9.4f}"
            + Fore.WHITE
        )

    print()
    for remaining in range(DISPLAY_WAIT_TIME, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write(f"  Refresh: {remaining:3d} seconds remaining.")
        sys.stdout.flush()
        sleep(1)

    print("   ... retrieving services ...")


def main():

    parser = argparse.ArgumentParser(description="Service Status display")
    parser.add_argument(
        "-H",
        "--name",
        required=True,
        help="Name of the service for getting status",
    )
    args = parser.parse_args()
    name = args.name

    previous_service_status = list()
    while True:
        service_status = get_service_status(name)
        if "status" in service_status and "service" in service_status:
            print_service_status(service_status["service"], service_status["status"], previous_service_status)
            previous_service_status = service_status["status"]
        else:
            print(f"Error getting service status for {name}!")
            sleep(DISPLAY_WAIT_TIME)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting service-status-display")
        exit()
