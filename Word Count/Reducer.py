from concurrent import futures
import grpc
import ProtoFiles.master_pb2 as master_pb2
import ProtoFiles.master_pb2_grpc as master_pb2_grpc
import sys

class Reducer(master_pb2_grpc.MasterServiceServicer):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def reduce(self, request, context):
        # get the name.txt file, and add up all the values of same keys and write to output_name.txt
        with open(self.name+'.txt', 'r') as f:
            lines = f.readlines()
            keyValues = {}
            for line in lines:
                key, value = line.split()
                if key in keyValues:
                    keyValues[key] += int(value)
                else:
                    keyValues[key] = int(value)

            with open('output_'+self.name+'.txt', 'w') as f:
                for key, value in keyValues.items():
                    f.write(key + ' ' + value + '\n')

        return master_pb2.ReducerResponse(status='Reducer Finished')


if __name__ == "__main__":
    name = sys.argv[1]
    port = sys.argv[2]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    master_pb2_grpc.add_MasterServiceServicer_to_server(Reducer(name), server)
    server.add_insecure_port('[::]:' + port)
    server.start()

# python -m grpc_tools.protoc -I./  --python_out=ProtoFiles/ ./Master.proto --pyi_out=ProtoFiles/ --grpc_python_out=ProtoFiles/
