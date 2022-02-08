import subprocess
import argparse
import re
from datetime import datetime, timedelta
from time import sleep
import socket
import requests
import scapy.all as scapy
from concurrent.futures import ThreadPoolExecutor

MONITOR_INTERVAL = 60
DISCOVERY_INTERVAL = 300

parser = argparse.ArgumentParser(description="Host Monitor")
parser.add_argument('--poolsize', default=10, help='Size of the threadpool')
parser.add_argument('--quokka', default="localhost:5001", help='Hostname/IP and port of the quokka server')

args = parser.parse_args()
threadpool_size = int(args.poolsize)
quokka = args.quokka


def get_hosts():

    global quokka

    print("\n\n----> Retrieving hosts ...", end="")
    try:
        response = requests.get("http://"+quokka+"/hosts")
    except requests.exceptions.ConnectionError as e:
        print(f" !!!  Exception trying to get hosts via REST API: {e}")
        return {}

    if response.status_code != 200:
        print(f" !!!  Failed to retrieve hosts from server: {response.reason}")
        return {}

    print(" Hosts successfully retrieved")
    return response.json()


def discovery():

    # DISCOVER HOSTS ON NETWORK USING ARPING FUNCTION
    print(
        "\n\n----- Discovery hosts on network using arping() function ---------------------"
    )
    ans, unans = scapy.arping("10.0.0.0/24")
    ans.summary()

    for res in ans.res:
        print(f"oooo> IP address discovered: {res[0].payload.pdst}")

        ip_addr = res[1].payload.psrc
        mac_addr = res[1].payload.hwsrc
        try:
            hostname = socket.gethostbyaddr(str(ip_addr))
        except (socket.error, socket.gaierror):
            hostname = (str(ip_addr), [], [str(ip_addr)])
        last_heard = str(datetime.now())[:-3]

        host = {
            "ip_address": ip_addr,
            "mac_address": mac_addr,
            "hostname": hostname[0],
            "last_heard": last_heard,
            "availability": True,
            "response_time": 0
        }
        update_host(host)


def update_host(host):

    global quokka

    print(f"----> Updating host status via REST API: {host['hostname']}", end="")
    try:
        rsp = requests.put("http://"+quokka+"/hosts", params={"hostname": host["hostname"]}, json=host)
    except requests.exceptions.ConnectionError as e:
        print(f" !!!  Exception trying to update host {host['hostname']} via REST API: {e}")
        return

    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error posting to /hosts, response: {rsp.status_code}, {rsp.content}"
        )
        print(f" !!!  Unsuccessful attempt to update host status via REST API: {host['hostname']}")
    else:
        print(f" Successfully updated host status via REST API: {host['hostname']}")


def get_response_time(ping_output):

    m = re.search(r"time=([0-9]*)", ping_output)
    if m.group(1).isnumeric():
        return str(float(m.group(1))/1000)
    else:
        return 0


def ping_host(host):

    try:
        print(f"----> Pinging host: {host['hostname']}", end="")
        ping_output = subprocess.check_output(
            ["ping", "-c3", "-n", "-i0.5", "-W2", host["ip_address"]]
        )
        host["availability"] = True
        host["response_time"] = get_response_time(str(ping_output))
        host["last_heard"] = str(datetime.now())[:-3]
        print(f" Host ping successful: {host['hostname']}")

    except subprocess.CalledProcessError:
        host["availability"] = False
        print(f" !!!  Host ping failed: {host['hostname']}")

    update_host(host)


def main():

    global threadpool_size

    last_discovery = datetime.now()-timedelta(days=1)
    while True:

        if (datetime.now() - last_discovery).total_seconds() > DISCOVERY_INTERVAL:
            discovery()
            last_discovery = datetime.now()

        hosts = get_hosts()
        with ThreadPoolExecutor(max_workers=threadpool_size) as executor:
            executor.map(ping_host, hosts.values())

        sleep(MONITOR_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting host-monitor")
        exit()
