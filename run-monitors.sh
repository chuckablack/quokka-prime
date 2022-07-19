#!/bin/bash
echo "hello I'm running monitors here!"
#cd monitors ; ./run-monitors.sh 172.17.0.3:5001
cd monitors ; python3 service_monitor.py --quokka 192.168.147.109:5001
