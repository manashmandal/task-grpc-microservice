# Python gRPC-based microservice

## Functional Requirements

- gRPC Server that serves the time based electricity consumption data
- HTTP Server that will request data from gRPC and deliver the data as JSON
- Single Page HTML Document that requests the JSON from the HTTP Server and displays it

## How to run the project with Docker and docker-compose

Clone the project and make sure that `docker` and `docker-compose` is installed. Then use the following commands.

```
docker-compose build
docker-compose up
```

The html page will be served at `localhost:5000` address.

## How to run without Docker

Install the requirement using `pip install -r requirements.txt`.

- Open a terminal and use `bash run_server_debug_mode.sh` to run the http server.
- And to start grpc server go to the `grpc_server` directory then run `python server.py`
- Now visit `http://localhost:5000` to see the html page and click the button to fetch data.

## Project Structure

The project is structured between three parts. The shared `protos` directory which contains the protobuf schema definitions, `grpc_server` and a Flask based `http server` which is located at the root of the directory.

There are some tests written in `tests` directory which can be run by `pytest` command.

```
Project Directory
|--- protos
|--- grpc_server
|--- tests
|--- templates
app.py (Flask based HTTP Server | Also serves the html page)
```

There are some bash files are written for development purpose to automate the process of generating python files each time protobuf schema was changed.

## gRPC Service Method

Here **gRPC Server Streaming** method was used.

## Workflow

The Flask app is rendering a html file and communicating with the gRPC Server. On sending a request to Flask App `/usage/data` endpoint, it makes a RPC to the gRPC Server and iterates over the response to generate a fixed length list of dictionaries and then serialize to JSON and send back to the client.

## Demo

<img src="/public/demo.gif?raw=true">
