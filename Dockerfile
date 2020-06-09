#FROM python:3-alpine
FROM ubuntu:latest
RUN apt-get update -y && apt-get install software-properties-common -y && apt-add-repository universe && apt-get install -y python3 python3-pip build-essential libpq-dev
WORKDIR /code
ENV FLASK_APP Rest/Resources.py
ENV FLASK_RUN_HOST 127.0.0.1
#RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#RUN pip3 install -r requirements.txt
COPY . .
RUN python3 GenerateKeysRSA.py
CMD ["flask","run"]
#CMD ["python3", "Rest/Resources.py"]
