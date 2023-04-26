from concurrent import futures
import grpc
import reducer_pb2 as reducer_pb2
import reducer_pb2_grpc as reducer_pb2_grpc
import sys

class Reducer(reducer_pb2_grpc.ReducerServicer):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def reduce(self, request, context):
        self.outputLocation = request.outputLocation
        self.count_M = request.count_M
        index = request.index
        f = open('ouuuu.txt', 'w')
        f.write('hehe')
        for j in range(self.count_M):
            with open(self.outputLocation + 'M' + str(j) + +'_P'+index+'.txt', 'r') as f:
                lines = f.readlines()
                keyValues = {}
                for line in lines:
                    key, value = line.split()
                    if key in keyValues:
                        keyValues[key] += int(value)
                    else:
                        keyValues[key] = int(value)

        with open(self.outputLocation + 'output_'+self.name+'.txt', 'w') as f:
            for key, value in keyValues.items():
                f.write(key + ' ' + value + '\n')


if __name__ == "__main__":
    name = sys.argv[1]
    port = sys.argv[2]
    print(name, port)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reducer_pb2_grpc.add_ReducerServicer_to_server(Reducer(name), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()

# python -m grpc_tools.protoc -I./  --python_out=ProtoFiles/ ./Master.proto --pyi_out=ProtoFiles/ --grpc_python_out=ProtoFiles/
