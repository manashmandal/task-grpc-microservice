FROM python:3.8-buster

WORKDIR /app

COPY requirements.txt .

RUN apt update

RUN pip install -r requirements.txt

COPY protos/ protos/

RUN python -m grpc_tools.protoc -I protos/ --python_out=. --grpc_python_out=. protos/meterusage.proto

EXPOSE 5000

COPY . .

