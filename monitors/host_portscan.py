from datetime import datetime
import argparse
from time import sleep
import requests
import nmap
from concurrent.futures import ThreadPoolExecutor

MONITOR_INTERVAL = 300

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

    hosts = response.json()
    print(f" {len(hosts)} hosts successfully retrieved")
    return hosts


def update_host(host):

    global quokka

    print(f"----> Updating host status via REST API: {host['hostname']}", end="")
    try:
        rsp = requests.put("http://"+quokka+"/hosts", params={"hostname": host["hostname"]}, json=host)
    except requests.exceptions.ConnectionError as e:
        print(f" !!!  Exception trying to update host {host['hostname']}  via REST API: {e}")
        return

    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error posting to /hosts, response: {rsp.status_code}, {rsp.content}"
        )
        print(f" !!!  Unsuccessful attempt to update host status via REST API: {host['hostname']}")
    else:
        print(f" Successfully updated host status via REST API: {host['hostname']}")


def portscan_hosts(host):

    if "availability" not in host or not host["availability"]:
        return

    ip = host["ip_address"]
    print(f"====> Scanning host: {host['hostname']} at IP: {ip}")
    nm = nmap.PortScanner()
    nm.scan(ip, '22-1024')

    try:
        nm[ip]
    except KeyError as e:
        print(f" !!!  Scan failed: {e}")
        return

    print(f"===> Scan results: {nm[ip].all_tcp()}")
    host["open_tcp_ports"] = str(nm[ip].all_tcp())
    update_host(host)


def main():

    global threadpool_size

    while True:

        hosts = get_hosts()
        with ThreadPoolExecutor(max_workers=threadpool_size) as executor:
            executor.map(portscan_hosts, hosts.values())

        sleep(MONITOR_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting host-portscan")
        exit()
