import meterusage_pb2
import meterusage_pb2_grpc
import grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = meterusage_pb2_grpc.MeterUsageServiceStub(channel)
        response_iterator = stub.GetMeterUsage(meterusage_pb2.MeterUsageRequest())
        for response in response_iterator:
            print(response)


run()
