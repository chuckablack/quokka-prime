name=${1:-localhost}
broker=${2:-localhost}
sudo python3 quokka_worker.py --name $name --broker $broker
