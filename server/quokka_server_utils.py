from urllib.parse import urlparse
from ipaddress import IPv4Address
import socket


def get_hostname_from_target(target):

    # Target could be a URL; if so, use urlparse to extract the network location (hostname)
    if target.startswith("http://") or target.startswith("https://"):
        parsed_target = urlparse(target)
        return parsed_target.netloc

    return target


def get_ip_address_from_target(target):

    try:
        IPv4Address(target)  # Exception thrown if not an IP address
        return target  # If we got here, it is already an IP address

    except ValueError:
        hostname = get_hostname_from_target(target)  # Get the hostname part of the target
        try:
            return socket.gethostbyname(hostname)  # Attempt to get IP address and return it
        except (socket.error, socket.gaierror) as e:
            return None  # If getting IP address failed, return None
