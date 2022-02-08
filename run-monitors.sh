#!/bin/bash
echo "hello I'm running monitors here!"
#cd monitors ; ./run-monitors.sh 172.17.0.3:5001
cd monitors ; python3 service_monitor.py --quokka 172.17.0.4:5001
