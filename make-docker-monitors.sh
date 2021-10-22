sudo docker stop quokka-prime-monitors
sudo docker container rm quokka-prime-monitors
sudo docker image rm quokka-prime-monitors

sudo docker build -f dockerfile-monitors --tag quokka-prime-monitors .
sudo docker run -e PYTHONUNBUFFERED=1 --name quokka-prime-monitors quokka-prime-monitors
