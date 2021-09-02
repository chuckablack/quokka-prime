from extensions import db
from datetime import datetime
from pprint import pformat
import time


def remove_internals(d):

    if d: return {k: v for (k, v) in d.items() if not k.startswith("_")}
    else: return None


def get_all_hosts():

    hosts = {host["hostname"]: remove_internals(host) for host in db.hosts.find()}
    return hosts


def get_host(hostname):

    host = db.hosts.find_one({"hostname": hostname})
    return remove_internals(host)


def get_host_status(hostname, datapoints):

    status_records = db.hosts_status.find({"hostname": hostname}).sort("time", -1).limit(datapoints)
    return [remove_internals(status_record) for status_record in status_records]


def get_host_status_summary(hostname, datapoints):

    status_records = db.hosts_status_summary.find({"hostname": hostname}).sort("time", -1).limit(datapoints)
    return [remove_internals(status_record) for status_record in status_records]


def set_host(host):

    existing_host = db.hosts.find_one({"hostname": host["hostname"]})
    if not existing_host:
        db.hosts.insert_one(host)
    else:
        db.hosts.update_one({"hostname": host["hostname"]}, {"$set": host})

    host_status = {
        "time": str(datetime.now())[:-3],
        "hostname": host["hostname"],
        "availability": host["availability"],
        "response_time": host["response_time"]
    }
    db.hosts_status.insert_one(host_status)


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

    service_status = {
        "time": str(datetime.now())[:-3],
        "name": service["name"],
        "availability": service["availability"],
        "response_time": service["response_time"]
    }
    db.services_status.insert_one(service_status)


def get_service_status(name, datapoints):

    status_records = db.services_status.find({"name": name}).sort("time", -1).limit(datapoints)
    return [remove_internals(status_record) for status_record in status_records]


def get_service_status_summary(name, datapoints):

    status_records = db.services_status_summary.find({"name": name}).sort("time", -1).limit(datapoints)
    return [remove_internals(status_record) for status_record in status_records]


def get_all_devices():

    devices = {device["name"]: remove_internals(device) for device in db.devices.find()}
    return devices


def get_device(name):

    device = db.devices.find_one({"name": name})
    return remove_internals(device)


def get_device_status(name, datapoints):

    status_records = db.devices_status.find({"name": name}).sort("time", -1).limit(datapoints)
    return [remove_internals(status_record) for status_record in status_records]


def get_device_status_summary(name, datapoints):

    status_records = db.devices_status_summary.find({"name": name}).sort("time", -1).limit(datapoints)
    return [remove_internals(status_record) for status_record in status_records]


def set_device(device):

    existing_device = db.devices.find_one({"name": device["name"]})
    if not existing_device:
        db.devices.insert_one(device)
    else:
        db.devices.update_one({"name": device["name"]}, {"$set": device})

    device_status = {
        "time": str(datetime.now())[:-3],
        "name": device["name"],
        "availability": device["availability"],
        "response_time": device["response_time"]
    }
    db.devices_status.insert_one(device_status)


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


def record_snoop_data(snoop_data):

    for captured_packet in snoop_data["packets"]:

        packet = dict()
        packet["timestamp"] = str(datetime.now())[:-3]
        packet["local_timestamp"] = snoop_data["timestamp"]
        packet["source"] = snoop_data["source"]

        packet["packet_hexdump"] = captured_packet["hexdump"]
        packet["packet_json"] = pformat(captured_packet)

        db.snoop_captures.insert_one(packet)


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

    search_items = list()
    if ip: search_items.append({"$or": [{"ip_src": ip}, {"ip_dst": ip}]})
    if protocol: search_items.append({"protocol": protocol.upper()})
    if port: search_items.append({"$or": [{"sport": port}, {"dport": port}]})

    search = {"$and": search_items} if search_items else {}
    packets_with_internals = db.captures.find(search).sort("timestamp", -1).limit(num_packets)

    packets = list()
    for packet_to_clean in packets_with_internals:
        packet = remove_internals(packet_to_clean)
        packets.append(packet)

    return packets


def trim_tables(status_expire_after, diagnostics_expire_after):

    for status_table in [db.hosts_status, db.services_status, db.devices_status]:
        status_table.delete_many({"time": {"$lt": str(status_expire_after)}})

    for diagnostics_table in [db.captures, db.traceroutes, db.portscans]:
        diagnostics_table.delete_many({"timestamp": {"$lt": str(diagnostics_expire_after)}})


def create_summaries(hour):

    class StatusTableInfo:
        SEARCH_FIELD = "search_field"
        NAMES = "names"
        STATUS_TABLE = "status_table"
        STATUS_SUMMARY_TABLE = "status_summary_table"

    # Get names as identifiers for all status tables
    hostnames = [host["hostname"] for host in db.hosts.find()]
    servicenames = [service["name"] for service in db.services.find()]
    devicenames = [device["name"] for device in db.devices.find()]

    status_tables = [{StatusTableInfo.NAMES: hostnames,
                      StatusTableInfo.SEARCH_FIELD: "hostname",
                      StatusTableInfo.STATUS_TABLE: db.hosts_status,
                      StatusTableInfo.STATUS_SUMMARY_TABLE: db.hosts_status_summary},
                     {StatusTableInfo.NAMES: servicenames,
                      StatusTableInfo.SEARCH_FIELD: "name",
                      StatusTableInfo.STATUS_TABLE: db.services_status,
                      StatusTableInfo.STATUS_SUMMARY_TABLE: db.services_status_summary},
                     {StatusTableInfo.NAMES: devicenames,
                      StatusTableInfo.SEARCH_FIELD: "name",
                      StatusTableInfo.STATUS_TABLE: db.devices_status,
                      StatusTableInfo.STATUS_SUMMARY_TABLE: db.devices_status_summary},
                     ]

    for status_table_info in status_tables:
        generate_status_data_for_hour(status_table_info[StatusTableInfo.STATUS_TABLE],
                                      status_table_info[StatusTableInfo.NAMES],
                                      status_table_info[StatusTableInfo.SEARCH_FIELD],
                                      status_table_info[StatusTableInfo.STATUS_SUMMARY_TABLE],
                                      hour)


def generate_status_data_for_hour(status_table, names, search_field, status_summary_table, hour):

    for name in names:
        status_items_for_hour = status_table.find({search_field: name, "time": {'$regex': '^'+hour}})

        hourly_summary = dict()
        hourly_summary[search_field] = name
        hourly_summary["time"] = str(datetime.fromisoformat(hour))
        hourly_summary["availability"] = 0
        hourly_summary["response_time"] = 0

        num_availability_records = 0
        num_response_time_records = 0

        availability = 0
        response_time = 0.0

        for status_item in status_items_for_hour:
            num_availability_records += 1
            if status_item["availability"]:
                availability += 100
                response_time += float(status_item["response_time"])
                num_response_time_records += 1

        if num_availability_records > 0:
            hourly_summary["availability"] = availability / num_availability_records
        if num_response_time_records > 0:
            hourly_summary["response_time"] = response_time / num_response_time_records

        status_summary_table.insert_one(hourly_summary)
