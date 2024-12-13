import argparse
from datetime import datetime, timedelta
from time import sleep
import requests
from tplinkrouterc6u import TplinkRouter, TPLinkDecoClient

MONITOR_INTERVAL = 60

parser = argparse.ArgumentParser(description="Hostnames Monitor")
parser.add_argument('--quokka', default="localhost:5001", help='Hostname/IP and port of the quokka server')
parser.add_argument('--router', default="192.168.68.1", help='Subnet to be discovered/monitored')
parser.add_argument('--password', default="butch057!", help="Password to access the router's API")

args = parser.parse_args()
quokka = args.quokka
router = args.router
password = args.password


def get_router_devices():

    global router, password

    print("\n\n----> Retrieving hostnames from router...", end="")
    tplink_router = TPLinkDecoClient(f"http://{router}", password)
    tplink_router.authorize()

    status = tplink_router.get_status()
    if status:
        devices = status.devices
    else:
        devices = []

    tplink_router.logout()
    return devices


def update_hostname(ip, hostname):

    global quokka

    print(f"----> Updating hostnames via REST API: {ip}={hostname}", end="")
    try:
        rsp = requests.get("http://"+quokka+"/hostname", params={"ip": ip})
        rsp = requests.put("http://"+quokka+"/hostname", params={"ip": ip, "hostname": hostname})
    except requests.exceptions.ConnectionError as e:
        print(f" !!!  Exception trying to update ip {ip} with hostname {hostname} via REST API: {e}")
        return

    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error posting to /hostname, response: {rsp.status_code}, {rsp.content}"
        )
        print(f" !!!  Unsuccessful attempt to update host status via REST API: {ip}={hostname}")
    else:
        print(f" Successfully updated hostname via REST API: {ip}={hostname}")


def main():

    last_discovery = datetime.now()-timedelta(days=1)
    while True:

       devices = get_router_devices()
       for device in devices:
           mac = device.macaddr
           ip = device.ipaddr
           hostname = device.hostname
           print(f"ip: {ip}, hostname: {hostname}, mac: {mac}")

           update_hostname(device.ipaddr, device.hostname)

       sleep(MONITOR_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting hostnames-monitor")
        exit()
