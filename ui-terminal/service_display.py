import os
import subprocess
import sys
import argparse
from time import sleep
from colorama import Fore
import requests
from quokka_constants import DISPLAY_WAIT_TIME

parser = argparse.ArgumentParser(description="Service Display")
parser.add_argument('--quokka', default="localhost:5001", help='Hostname/IP and port of the quokka server')

args = parser.parse_args()
quokka = args.quokka


def get_services():

    try:
        response = requests.get(f"http://{quokka}/services")
    except requests.ConnectionError as e:
        print(f"!!! connection error: {e}")
        return {}

    if response.status_code != 200:
        print(f"get services failed: {response.reason}")
        return {}

    return response.json()


def print_services(services, previous_services):

    subprocess.call("clear" if os.name == "posix" else "cls")
    print(
        "\n  __Service_Name___________   __Type__  ________Target_________ "
        + " ________Data______ _Avail_ ___Rsp_  __Last_Heard___________\n"
    )
    for service in services.values():

        if not service["availability"]:
            color = Fore.RED
        elif float(service["response_time"]) > float(service["sla_response_time"]):
            color = Fore.LIGHTCYAN_EX
        elif service["name"] in previous_services and service == previous_services[service["name"]]:
            color = Fore.GREEN
        else:
            color = Fore.LIGHTGREEN_EX

        print(
            color +
            f"  {service['name'][:26]:<26}"
            + f"   {service['type']:>6}"
            + f"   {service['target'][:22]:<22}"
            + f"   {service['data'][:18]:>18}"
            + f"   {str(service['availability']):>5}"
            + f"   {service['response_time']:>5}"
            + f"  {service['last_heard']:>16}"
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

    previous_services = dict()
    while True:
        services = get_services()
        print_services(services, previous_services)
        previous_services = services


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting service-display")
        exit()
