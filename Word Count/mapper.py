import sys
from concurrent import futures
import grpc
import ProtoFiles.mapper_pb2 as mapper_pb2
import ProtoFiles.mapper_pb2_grpc as mapper_pb2_grpc
import ProtoFiles.master_pb2 as master_pb2
import ProtoFiles.master_pb2_grpc as master_pb2_grpc


class Mapper(mapper_pb2_grpc.ServerServicer):
    def __init__(self, name, port):
        super().__init__()
        self.name = name
        self.port = port

    def map(self, request, context):
        self.reducers = request.reducers
        filenames = request.filenames

        keyVPairs = []
        for filename in filenames:
            with open(filename, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    for word in line.split():
                        keyVPairs.append((word, 1))

        self.partitionStrategy(keyVPairs)
        self.notifyMaster()
    
    def notifyMaster(self):
        with grpc.insecure('localhost:8888') as channel:
            stub = master_pb2_grpc.MasterServiceStub(channel)
            response = stub.mapperFinished(master_pb2.MapperFinishedRequest())
            print('Mapper Done')
            
    def partitionStrategy(self, keyVPairs):
        for tuple in keyVPairs:
            hash = int(hash(tuple[0]))
            reducer = hash % self.reducers
            with open('reducer_'+reducer+'.txt', 'a') as f:
                f.write(tuple[0] + ' ' + tuple[1] + '\n')

def main(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mapper_pb2_grpc.add_RegistryServerServicer_to_server(
        Mapper(name, port), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    name = sys.argv[0]
    port = sys.argv[1]
    main(name, port)
