from flask import Flask, jsonify, request
from flask_cors import CORS
import grpc
import meterusage_pb2, meterusage_pb2_grpc
import os
from itertools import islice

app = Flask(__name__)

# Allowing all origin for the time being
CORS(app)

GRPC_SERVER = os.environ.get("GRPC_SERVER", "localhost:50051")


@app.route("/usage/data", methods=["GET"])
def get_usage_data_from_grpc_server():
    """
    This route is used to get the usage data from the grpc server and serialize it to JSON.
    """
    usage_data = []
    limit = int(request.args.get("limit", -1))
    offset = int(request.args.get("offset", 0))
    with grpc.insecure_channel(GRPC_SERVER) as channel:
        stub = meterusage_pb2_grpc.MeterUsageServiceStub(channel)
        response_iterator = stub.GetMeterUsage(meterusage_pb2.MeterUsageRequest())

        # If limit is provided, slicing the list based on limit and offset
        if limit > 0:
            response_iterator = islice(response_iterator, offset, limit + offset)

        response: meterusage_pb2.MeterUsageResponse
        for response in response_iterator:
            usage_data.append(
                {
                    "time": response.time.ToDatetime(),
                    "usage": response.meterusage,
                }
            )

    return jsonify({"data": usage_data, "status": "success"}), 200
