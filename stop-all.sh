pkill flask
pkill node
ps -ef | grep quokka_worker | grep -v grep | awk '{print $2}' | xargs sudo kill
cd monitor
./stop-monitor-all.sh
