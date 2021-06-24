quokka=${1:-localhost:5001}
sudo python3 host_monitor.py --quokka $quokka &
sudo python3 host_portscan.py --quokka $quokka &
python3 device_monitor.py --quokka $quokka &
python3 service_monitor.py --quokka $quokka &
