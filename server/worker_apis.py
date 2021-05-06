from datetime import datetime
import pika
import json


def start_portscan(target):

    print(f"starting portscan for target: {target}")
    token = str(datetime.now())
    portscan_info = {
        "quokka": "localhost:5001",
        "work_type": "portscan",
        "target": target,
        "token": token,
    }
    portscan_info_json = json.dumps(portscan_info)
    send_worker_request("localhost", portscan_info_json)
    return token


def start_traceroute(target):

    print(f"starting traceroute for: {target}")

    token = str(datetime.now())
    traceroute_info = {
        "quokka": "localhost:5001",
        "work_type": "traceroute",
        "target": target,
        "token": token,
    }
    traceroute_info_json = json.dumps(traceroute_info)
    send_worker_request("localhost", traceroute_info_json)
    return token


def start_capture(ip, protocol, port, capture_time):

    print(f"starting capture for ip: {ip}, protocol: {protocol}, port: {port}, time: {capture_time}")

    capture_info = {
        "quokka": "localhost:5001",
        "work_type": "capture",
        "ip": ip,
        "protocol": protocol,
        "port": port,
        "capture_time": capture_time,
    }
    capture_info_json = json.dumps(capture_info)
    send_worker_request("localhost", capture_info_json)


def send_worker_request(broker, message):

    connection = pika.BlockingConnection(pika.ConnectionParameters(broker))
    channel = connection.channel()
    channel.queue_declare(queue="quokka-worker", durable=True)
    channel.basic_publish(
        exchange="", routing_key="quokka-worker", body=message
    )
