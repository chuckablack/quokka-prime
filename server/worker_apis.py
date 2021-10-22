from datetime import datetime
import pika
import json
import socket
import yaml
from ipaddress import IPv4Address, IPv4Network

DEFAULT_KEY = "0.0.0.0/0"


def get_my_ip_address():

    # Note: if your hostname is in /etc/hosts you must comment it out
    ip_address = socket.gethostbyname(socket.gethostname())
    return ip_address if ip_address else "localhost"


def start_portscan(target):

    print(f"starting portscan for target: {target}")
    token = str(datetime.now())
    portscan_info = {
        "quokka": get_my_ip_address() + ":5001",
        "work_type": "portscan",
        "target": target,
        "token": token,
    }
    portscan_info_json = json.dumps(portscan_info)
    send_worker_request("localhost", portscan_info_json, key=target)
    return token


def start_traceroute(target):

    print(f"starting traceroute for: {target}")

    token = str(datetime.now())
    traceroute_info = {
        "quokka": get_my_ip_address() + ":5001",
        "work_type": "traceroute",
        "target": target,
        "token": token,
    }
    traceroute_info_json = json.dumps(traceroute_info)
    send_worker_request("localhost", traceroute_info_json, key=target)
    return token


def start_capture(ip, protocol, port, capture_time):

    print(f"starting capture for ip: {ip}, protocol: {protocol}, port: {port}, time: {capture_time}")

    capture_info = {
        "quokka": get_my_ip_address() + ":5001",
        "work_type": "capture",
        "ip": ip,
        "protocol": protocol,
        "port": port,
        "capture_time": capture_time,
    }
    capture_info_json = json.dumps(capture_info)
    send_worker_request("localhost", capture_info_json, key=ip)


def send_worker_request(broker, message, key):

    print(f"looking for worker for key: {key}")
    worker_name = find_worker_name(key)
    print(f"worker name: {worker_name}")

    connection = pika.BlockingConnection(pika.ConnectionParameters(broker))
    channel = connection.channel()
    channel.queue_declare(queue=worker_name, durable=True)
    channel.basic_publish(
        exchange="", routing_key=worker_name, body=message
    )


def find_worker_name(key):

    with open("../monitors/workers.yaml", "r") as yaml_in:
        yaml_workers = yaml_in.read()
        workers = yaml.safe_load(yaml_workers)

    try:
        IPv4Address(key)  # Exception thrown if not an IP address
        search_worker_key = str(IPv4Network(key+"/24", strict=False))
        print(f"found subnet address: {search_worker_key}")
    except ValueError:
        search_worker_key = key
        print(f"subnet address not found, using key: {key}")

    if search_worker_key in workers:
        return workers[search_worker_key]["worker-name"]
    elif DEFAULT_KEY in workers:
        print(f"looking for default key {DEFAULT_KEY} in workers {workers}")
        return workers[DEFAULT_KEY]["worker-name"]
    else:
        return "quokka-worker"
