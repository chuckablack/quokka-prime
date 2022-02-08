sudo docker stop quokka-prime-server
sudo docker container rm quokka-prime-server
sudo docker image rm quokka-prime-server

sudo docker build -f dockerfile-server --tag quokka-prime-server .
sudo docker run -e PYTHONUNBUFFERED=1 -e mongo=172.17.0.2:27017 --name quokka-prime-server quokka-prime-server
