import grpc
import meterusage_pb2
import meterusage_pb2_grpc
from concurrent import futures
from multiprocessing import cpu_count
import logging
from google.protobuf.timestamp_pb2 import Timestamp
import datetime
import csv
from dateutil import parser
import os


class MeterUsage(meterusage_pb2_grpc.MeterUsageService):
    def GetMeterUsage(
        self, request: meterusage_pb2.MeterUsageRequest, context: grpc.ServicerContext
    ):
        # Reading the csv file and returning the data via server streaming
        with open(
            os.path.join(os.getcwd(), "data", "meterusage.1643022756.csv")
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Returning current datetime if no timestamp is provided
                parsed_datetime = parser.parse(row.get("time", datetime.datetime.now()))
                timestamp = Timestamp()
                timestamp.FromDatetime(parsed_datetime)
                # Returning value 0 if no value is provided
                meterusage = float(row.get("meterusage", 0))
                yield meterusage_pb2.MeterUsageResponse(
                    time=timestamp,
                    meterusage=meterusage,
                )


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=cpu_count()))
    meterusage_pb2_grpc.add_MeterUsageServiceServicer_to_server(MeterUsage(), server)
    server.add_insecure_port("[::]:50051")
    logging.info("Starting server on port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
