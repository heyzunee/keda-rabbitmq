FROM python:3.8-slim

RUN mkdir /main
WORKDIR /main

COPY requirements.txt .
RUN apt-get -y update \
    && apt-get -y install git gcc python3-dev nano vim\
    && pip install --no-cache -r requirements.txt

COPY scripts ./scripts
RUN chmod +x ./scripts/*.sh

COPY src ./src

EXPOSE 8080
CMD ["./scripts/run.sh"]
