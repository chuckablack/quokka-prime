from extensions import db
from datetime import datetime
from pprint import pformat
import time


def remove_internals(d):

    return {k: v for (k, v) in d.items() if not k.startswith("_")}


def get_all_hosts():

    hosts = {host["hostname"]: remove_internals(host) for host in db.hosts.find()}
    return hosts


def get_host(hostname):

    host = db.hosts.find_one({"hostname": hostname})
    return remove_internals(host)


def set_host(host):

    existing_host = db.hosts.find_one({"hostname": host["hostname"]})
    if not existing_host:
        db.hosts.insert_one(host)
    else:
        db.hosts.update_one({"hostname": host["hostname"]}, {"$set": host})


def get_all_services():

    services = {service["name"]: remove_internals(service) for service in db.services.find()}
    return services


def get_service(name):

    service = db.services.find_one({"name": name})
    return remove_internals(service)


def set_service(service):

    existing_service = db.services.find_one({"name": service["name"]})
    if not existing_service:
        db.services.insert_one(service)
    else:
        db.services.update_one({"name": service["name"]}, {"$set": service})


def get_all_devices():

    devices = {device["name"]: remove_internals(device) for device in db.devices.find()}
    return devices


def set_device(device):

    existing_device = db.devices.find_one({"name": device["name"]})
    if not existing_device:
        db.devices.insert_one(device)
    else:
        db.devices.update_one({"name": device["name"]}, {"$set": device})


def record_portscan_data(portscan_data):

    db.portscans.insert_one(portscan_data)


def record_traceroute_data(traceroute_data):

    db.traceroutes.insert_one(traceroute_data)


def record_capture_data(capture_data):

    for captured_packet in capture_data["packets"]:

        packet = dict()
        packet["timestamp"] = str(datetime.now())[:-3]
        packet["local_timestamp"] = capture_data["timestamp"]
        packet["source"] = capture_data["source"]

        if "Ethernet" in captured_packet:
            if "dst" in captured_packet["Ethernet"]:
                packet["ether_dst"] = captured_packet["Ethernet"]["dst"]
            if "src" in captured_packet["Ethernet"]:
                packet["ether_src"] = captured_packet["Ethernet"]["src"]

        if "IP" in captured_packet:
            if "dst" in captured_packet["IP"]:
                packet["ip_dst"] = captured_packet["IP"]["dst"]
            if "src" in captured_packet["IP"]:
                packet["ip_src"] = captured_packet["IP"]["src"]

        if "TCP" in captured_packet:
            packet["protocol"] = "TCP"
            if "dport" in captured_packet["TCP"]:
                packet["dport"] = captured_packet["TCP"]["dport"]
            if "sport" in captured_packet["TCP"]:
                packet["sport"] = captured_packet["TCP"]["sport"]

            if packet["sport"] == 443 or packet["dport"] == 443:
                packet["protocol"] = "HTTPS"
            elif packet["sport"] == 80 or packet["dport"] == 80:
                packet["protocol"] = "HTTP"

        elif "UDP" in captured_packet:
            packet["protocol"] = "UDP"
            if "dport" in captured_packet["UDP"]:
                packet["dport"] = captured_packet["UDP"]["dport"]
            if "sport" in captured_packet["UDP"]:
                packet["sport"] = captured_packet["UDP"]["sport"]

            if packet["sport"] == 123 or packet["dport"] == 123:
                packet["protocol"] = "NTP"

            if packet["sport"] == 67 or packet["dport"] == 67 or packet["sport"] == 68 or packet["dport"] == 68:
                packet["protocol"] = "DHCP"

        if "DNS" in captured_packet:
            packet["protocol"] = "DNS"
        elif "ARP" in captured_packet:
            packet["protocol"] = "ARP"
        elif "ICMP" in captured_packet:
            packet["protocol"] = "ICMP"

        packet["packet_hexdump"] = captured_packet["hexdump"]
        packet["packet_json"] = pformat(captured_packet)

        db.captures.insert_one(packet)


def get_portscan(target, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        scan = db.portscans.find_one({"target": target, "token": token})
        if not scan:
            time.sleep(5)
            continue

        return remove_internals(scan)

    return {}  # portscan results never found


def get_traceroute(target, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        traceroute = db.traceroutes.find_one({"target": target, "token": token})
        if not traceroute:
            time.sleep(5)
            continue

        return remove_internals(traceroute)

    return {}  # traceroute results never found


def get_capture(ip, protocol, port, num_packets):

    print(f"---> getting capture: {ip}, {protocol}, {port}, type: {type(port)}")

    # We must generate and implement specific queries based on what has been requested
    # Note that if we add more fields, we'll have to modify this simple method to handle all cases
    if ip and not protocol:  # Note that if not protocol, port isn't relevant
        search = {"$or": [{"ip_src": ip}, {"ip_dst": ip}]}
    elif ip and protocol and not port:
        search = {"$or": [{"ip_src": ip}, {"ip_dst": ip}], "protocol": protocol.upper()}
    elif ip and protocol and port:
        search = {
            "$and": [
                {"$or": [{"ip_src": ip}, {"ip_dst": ip}]},
                {"protocol": protocol.upper()},
                {"$or": [{"sport": port}, {"dport": port}]},
            ]
        }
    elif not ip and protocol and not port:
        search = {"protocol": protocol.upper()}
    elif not ip and protocol and port:
        search = {"protocol": protocol.upper(), "$or": [{"sport": port}, {"dport": port}]}
    elif not ip and not protocol and port:
        search = {"$or": [{"sport": port}, {"dport": port}]}
    else:  # Not sure what was requested, so just get everything
        search = {}

    packets_with_internals = db.captures.find(search).sort("timestamp", -1).limit(num_packets)

    packets = list()
    for packet_to_clean in packets_with_internals:
        packet = remove_internals(packet_to_clean)
        packets.append(packet)

    return packets
