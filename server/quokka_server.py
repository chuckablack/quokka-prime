from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource
from quokka_server_utils import get_hostname_from_target, get_ip_address_from_target
from DbHourlyTask import DbHourlyTask

from apidoc_models import ApiModels
import threading
import atexit

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

quokka_app = Flask(__name__)
CORS(quokka_app)

api = Api(quokka_app, version="1.0", title="Quokka", description="Quokka for 52-weeks-of-python",
          default="quokka", default_label="")
ApiModels.set_api_models(api)

from db_apis import get_all_hosts, set_host, get_host, get_host_status, get_host_status_summary
from db_apis import get_all_devices, set_device, get_device, get_device_status, get_device_status_summary
from db_apis import get_all_services, set_service, get_service, get_service_status, get_service_status_summary
from db_apis import get_capture, get_portscan, get_traceroute

from db_apis import record_portscan_data, record_traceroute_data, record_capture_data, record_snoop_data
from worker_apis import start_portscan, start_traceroute, start_capture, start_snoop

limiter = Limiter(quokka_app, key_func=get_remote_address)

# Start background DB hourly task
db_hourly_task = DbHourlyTask()
db_hourly_task_thread = threading.Thread(target=db_hourly_task.start)
db_hourly_task_thread.start()


# shutdown of our flask process requires terminating background db thread
def shutdown():

    db_hourly_task.set_terminate()
    db_hourly_task_thread.join()


atexit.register(shutdown)  # causes shutdown() to get called when exiting


@api.route("/hosts")
class HostsEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    @api.response(200, 'Success', ApiModels.hosts_response)
    def get():
        return get_all_hosts()

    @staticmethod
    @api.doc(params={"hostname": "Hostname of host to add or update"}, body=ApiModels.host_fields)
    @api.response(204, 'Success')
    @api.response(400, 'Must provide hostname to add/update host')
    def put():
        hostname = request.args.get("hostname")
        if not hostname:
            return "Must provide hostname to add/update host", 400

        host = request.get_json()
        set_host(host)
        return {}, 204


@api.route("/devices")
class DevicesEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    @api.response(200, 'Success', ApiModels.devices_response)
    def get():
        return get_all_devices()

    @staticmethod
    @api.doc(params={"name": "Name of device to add or update"}, body=ApiModels.device_fields)
    @api.response(204, 'Success')
    @api.response(400, 'Must provide device name to add/update service')
    def put():
        name = request.args.get("name")
        if not name:
            return "Must provide device name to add/update device", 400

        device = request.get_json()
        set_device(device)
        return {}, 204


@api.route("/services")
class ServicesEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    @api.response(200, 'Success', [ApiModels.services_response])
    def get():
        return get_all_services()

    @staticmethod
    @api.doc(params={"name": "Name of service to add or update"}, body=ApiModels.service_fields)
    @api.response(204, 'Success')
    @api.response(400, 'Must provide service name to add/update service')
    def put():
        name = request.args.get("name")
        if not name:
            return "Must provide service name to add/update service", 400

        service = request.get_json()
        set_service(service)
        return {}, 204


@api.route("/scan")
class ScanEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    @api.doc(params={"token": "The token returned from the corresponding POST that initiated the portscan",
                     "target": "The target for the portscan request"})
    @api.response(200, 'Success', ApiModels.portscan_data)
    @api.response(400, "Must provide token and target to get portscan")
    def get():
        target = request.args.get("target")
        if not target:
            return "Must provide target to get portscan", 400
        token = request.args.get("token")
        if not token:
            return "Must provide token to get portscan", 400

        return get_portscan(target, token)

    @staticmethod
    @api.doc(params={"target": "IP address or hostname of target host or device to scan"})
    @api.response(200, 'Success', ApiModels.token_response)
    @api.response(400, 'Must provide target to get portscan')
    def post():
        target = request.args.get("target")
        if not target:
            return "Must provide target to initiate portscan", 400
        token = start_portscan(target)
        return {"token": token}


@api.route("/worker/portscan")
class WorkerScanEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    @api.doc(body=ApiModels.portscan_data)
    @api.response(204, 'Success')
    def post():
        portscan_data = request.get_json()
        record_portscan_data(portscan_data)

        return {}, 204


@api.route("/traceroute")
class TracerouteEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    @api.doc(params={"token": "The token returned from the corresponding POST that initiated the traceroute",
                     "target": "The target for the traceroute request"})
    @api.response(400, "Must provide token and target to get traceroute")
    @api.response(200, 'Success', ApiModels.traceroute_data)
    def get():

        target = request.args.get("target")
        if not target:
            return "Must provide service target to get traceroute", 400
        hostname = get_hostname_from_target(target)

        token = request.args.get("token")
        if not token:
            return "Must provide token to get traceroute", 400
        return get_traceroute(hostname, token)

    @staticmethod
    @api.doc(params={"target": "IP address or hostname of target service, host, or device to find traceroute for"})
    @api.response(200, 'Success', ApiModels.token_response)
    @api.response(400, 'Must provide target to initiate traceroute')
    def post():
        target = request.args.get("target")
        if not target:
            return "Must provide  target to get traceroute", 400
        hostname = get_hostname_from_target(target)

        token = start_traceroute(hostname)
        return {"token": token}


@api.route("/worker/traceroute")
class WorkerTracerouteEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    @api.doc(body=ApiModels.traceroute_data)
    @api.response(204, 'Success')
    def post():
        traceroute_data = request.get_json()
        record_traceroute_data(traceroute_data)

        return {}, 204


@api.route("/capture")
class CaptureEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    @api.doc(params={"ip": "The ip address for which to capture packets",
                     "protocol": "The protocol for which to capture packets",
                     "port": "The port for which to capture packets",
                     "num_packets": "The number of packets to retrieve"})
    @api.response(200, 'Success', ApiModels.capture_data)
    def get():

        ip = request.args.get("ip")
        protocol = request.args.get("protocol")
        port = request.args.get("port")
        num_packets = request.args.get("num_packets")

        if ip: ip = get_ip_address_from_target(ip)

        if not num_packets or not num_packets.isnumeric(): num_packets = 10
        if port and port.isnumeric(): port = int(port)
        else: port = None

        return {"packets": get_capture(ip, protocol, port, int(num_packets))}

    @staticmethod
    @api.doc(params={"ip": "The ip address for which to capture packets",
                     "protocol": "The protocol for which to capture packets",
                     "port": "The port for which to capture packets",
                     "capture_time": "The time to capture packets"})
    @api.response(200, 'Capture initiated')
    def post():

        ip = request.args.get("ip")
        protocol = request.args.get("protocol")
        port = request.args.get("port")
        capture_time = request.args.get("capture_time")

        if ip: ip = get_ip_address_from_target(ip)

        if not capture_time: capture_time = 180
        else:  capture_time = int(capture_time)

        start_capture(ip, protocol, port, capture_time)
        return "Capture initiated", 200


@api.route("/worker/capture")
class WorkerCaptureEndpoint(Resource):

    @staticmethod
    @api.doc(body=ApiModels.capture_data)
    @api.response(204, 'Success')
    def post():
        capture_data = request.get_json()
        record_capture_data(capture_data)

        return {}, 204


@api.route("/snoop")
class SnoopEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    # @api.doc(params={"ip": "The ip address for which to snoop packets",
    #                  "protocol": "The protocol for which to snoop packets",
    #                  "port": "The port for which to snoop packets",
    #                  "num_packets": "The number of packets to retrieve"})
    @api.response(200, 'Success', ApiModels.snoop_data)
    def get():

        return {}

    @staticmethod
    @api.doc(params={"ip": "The ip address for which to snoop packets",
                     "protocol": "The protocol for which to snoop packets",
                     "port": "The port for which to snoop packets",
                     "snoop_time": "The time to snoop packets"})
    @api.response(200, 'Snoop initiated')
    def post():

        ip = request.args.get("ip")
        protocol = request.args.get("protocol")
        port = request.args.get("port")
        snoop_time = request.args.get("snoop_time")

        if ip: ip = get_ip_address_from_target(ip)

        if not snoop_time: snoop_time = 180
        else:  snoop_time = int(snoop_time)

        start_snoop(ip, protocol, port, snoop_time)
        return "Snoop initiated", 200


@api.route("/worker/snoop")
class WorkerSnoopEndpoint(Resource):

    @staticmethod
    @api.doc(body=ApiModels.snoop_data)
    @api.response(204, 'Success')
    def post():
        snoop_data = request.get_json()
        record_snoop_data(snoop_data)

        return {}, 204


@api.route("/host/status")
class HostStatusEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    @api.doc(params={"hostname": "Hostname of host to get status for",
                     "datapoints": "Number of datapoints to be returned"})
    @api.response(200, 'Success')
    @api.response(400, 'Must provide hostname to get host status')
    def get():
        hostname = request.args.get("hostname")
        datapoints = request.args.get("datapoints")

        if not hostname:
            return "Must provide hostname to get host status", 400
        if not datapoints:
            datapoints = "24"
        if not datapoints.isnumeric():
            return "Datapoints must be an integer", 400

        host = get_host(hostname)
        if not host:
            return f"Unknown host: {hostname}", 400

        host_status = {"host": host,
                       "status": get_host_status(hostname, int(datapoints)),
                       "summary": get_host_status_summary(hostname, int(datapoints))}
        return host_status, 200


@api.route("/service/status")
class ServiceStatusEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    @api.doc(params={"name": "Name of service to get status for",
                     "datapoints": "Number of datapoints to be returned"})
    @api.response(200, 'Success')
    @api.response(400, 'Must provide name to get service status')
    def get():
        name = request.args.get("name")
        datapoints = request.args.get("datapoints")

        if not name:
            return "Must provide name to get service status", 400
        if not datapoints:
            datapoints = "24"
        if not datapoints.isnumeric():
            return "Datapoints must be an integer", 400

        service = get_service(name)
        if not service:
            return f"Unknown service: {name}", 400

        service_status = {"service": service,
                          "status": get_service_status(name, int(datapoints)),
                          "summary": get_service_status_summary(name, int(datapoints))}
        return service_status, 200


@api.route("/device/status")
class DeviceStatusEndpoint(Resource):

    decorators = [limiter.limit("120/minute")]

    @staticmethod
    @api.doc(params={"name": "Name of device to get status for",
                     "datapoints": "Number of datapoints to be returned"})
    @api.response(200, 'Success')
    @api.response(400, 'Must provide name to get device status')
    def get():
        name = request.args.get("name")
        datapoints = request.args.get("datapoints")

        if not name:
            return "Must provide name to get device status", 400
        if not datapoints:
            datapoints = "24"
        if not datapoints.isnumeric():
            return "Datapoints must be an integer", 400

        device = get_device(name)
        if not device:
            return f"Unknown device: {name}", 400

        device_status = {"device": device,
                         "status": get_device_status(name, int(datapoints)),
                         "summary": get_device_status_summary(name, int(datapoints))}
        return device_status, 200
