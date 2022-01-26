import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import grpc
import meterusage_pb2, meterusage_pb2_grpc
from itertools import islice
from grpc._channel import _MultiThreadedRendezvous
import math

GRPC_SERVER = os.environ.get("GRPC_SERVER", "localhost:50051")


def create_app() -> Flask:
    """
    Simple factory function to create a Flask app
    """
    app = Flask(__name__)
    # Allowing all origin for the time being
    CORS(app)

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/usage/data", methods=["GET"])
    def get_usage_data_from_grpc_server():
        """
        This route is used to get the usage data from the grpc server and serialize it to JSON.
        """
        usage_data = []
        limit = int(request.args.get("limit", -1))
        offset = int(request.args.get("offset", 0))
        try:
            with grpc.insecure_channel(GRPC_SERVER) as channel:
                stub = meterusage_pb2_grpc.MeterUsageServiceStub(channel)
                response_iterator = stub.GetMeterUsage(
                    meterusage_pb2.MeterUsageRequest()
                )

                # If limit is provided, slicing the list based on limit and offset
                if limit > 0:
                    response_iterator = islice(
                        response_iterator, offset, limit + offset
                    )

                response: meterusage_pb2.MeterUsageResponse
                for response in response_iterator:
                    # if meterusage is NaN then set it to undefined
                    usage_data.append(
                        {
                            "time": response.time.ToDatetime(),
                            "meterusage": response.meterusage
                            if not math.isnan(response.meterusage)
                            else "undefined",
                        }
                    )

            return (
                jsonify({"data": usage_data, "status": "success", "message": ""}),
                200,
            )
        except _MultiThreadedRendezvous:
            return (
                jsonify(
                    {
                        "data": [],
                        "status": "error",
                        "message": "Failed to connect gRPC Server",
                    }
                ),
                500,
            )

    return app


app = create_app()
