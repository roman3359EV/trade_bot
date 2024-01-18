FROM python:3.10-alpine AS builder

RUN apk add tzdata
RUN ln -fs /usr/share/zoneinfo/Etc/GMT+3 /etc/localtime

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip3 install --no-cache-dir -r /requirements.txt

COPY ./src /src

CMD ["python3", "-m", "src.main"]

