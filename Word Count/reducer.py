from concurrent import futures
import grpc
import reducer_pb2 as reducer_pb2
import reducer_pb2_grpc as reducer_pb2_grpc
import sys
import os

class Reducer(reducer_pb2_grpc.ReducerServicer):
    def __init__(self, name):
        super().__init__()
        self.name = name

    
    def reduce(self, request, context):
        self.outputLocation = request.outputLocation
        self.count_M = request.count_M
        index = request.index

        keyValues = {}
        for j in range(self.count_M):
            with open(self.outputLocation + 'M' + str(j+1) +'_P'+str(index)+'.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    key, value = line.split()
                    if key in keyValues:
                        keyValues[key].append(int(value))
                    else:
                        keyValues[key] = [int(value)]
        # sort keyValues
        keyValues = dict(sorted(keyValues.items(), key=lambda item: item[0]))
        with open(self.outputLocation + 'output_'+ str(self.name)+'.txt', 'w') as f:
            for key, value in keyValues.items():
                values = keyValues[key]
                sum_ = sum(values)
                f.write(key + ' ' + str(sum_) + '\n')

        return reducer_pb2.ReducerResponse(status='Reducer Done')


if __name__ == "__main__":
    name = sys.argv[1]
    port = sys.argv[2]
    # print(name, port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reducer_pb2_grpc.add_ReducerServicer_to_server(Reducer(name), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()

# python -m grpc_tools.protoc -I./  --python_out=ProtoFiles/ ./Master.proto --pyi_out=ProtoFiles/ --grpc_python_out=ProtoFiles/
