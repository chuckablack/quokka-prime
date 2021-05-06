cd server
export FLASK_APP=quokka_server.py ; flask run --host 0.0.0.0 --port 5001
cd workers
sudo python3 quokka_server.py &
cd ../monitors
./run-monitors-all.sh &
cd ../ui
npm start &
