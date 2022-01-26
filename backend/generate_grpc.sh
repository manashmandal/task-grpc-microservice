python -m grpc_tools.protoc -I protos/ --python_out=$1 --grpc_python_out=$1 protos/meterusage.proto
python -m grpc_tools.protoc -I protos/ --python_out=$2 --grpc_python_out=$2 protos/meterusage.proto