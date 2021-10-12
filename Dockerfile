# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /quokka-prime

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "cd server" ]
CMD [ "./run-quokka.sh" ]
