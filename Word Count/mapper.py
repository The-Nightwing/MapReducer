import sys
from concurrent import futures
import grpc
import mapper_pb2 as mapper_pb2
import mapper_pb2_grpc as mapper_pb2_grpc
import master_pb2 as master_pb2
import master_pb2_grpc as master_pb2_grpc


class Mapper(mapper_pb2_grpc.MapperServicer):
    def __init__(self, name, port):
        super().__init__()
        self.name = name
        self.port = port

    def map(self, request, context):
        self.reducers = request.reducers
        filenames = request.filenames
        self.outputLocation = request.outputLocation

        for i in range(self.reducers):
            with open(self.outputLocation +'M'+str(self.name) +'_P'+str(i)+'.txt', 'w') as f:
                f.close()
                
        keyVPairs = []
        for filename in filenames:
            with open(filename, 'r') as f:
                lines = f.readlines()
                print(lines)
                for line in lines:
                    print(line.split())
                    for word in line.split():
                        keyVPairs.append((word.lower(), 1))

        self.partitionStrategy(keyVPairs)
        self.notifyMaster()
        return mapper_pb2.MapperResponse(status='Mapper Done')
    
    def notifyMaster(self):
        with grpc.insecure_channel('localhost:8888') as channel:
            stub = master_pb2_grpc.MasterStub(channel)
            response = stub.mapperFinished(master_pb2.Request(status='Mapper Done'))
            # print('Mapper Done')
    def HashFunction(self, string, reducers):
        sumD =0
        for i in range(len(string)):
             sumD += ord(string[i])
        return sumD%reducers
    
    def partitionStrategy(self, keyVPairs):   
            for tuple in keyVPairs:
                hash_ = self.HashFunction(tuple[0], self.reducers)
                reducer = hash_
                with open(self.outputLocation +'M'+str(self.name) +'_P'+str(reducer)+'.txt', 'a') as f:
                    f.write(str(tuple[0]) + ' ' + str(tuple[1]) + '\n')

def main(mame, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mapper_pb2_grpc.add_MapperServicer_to_server(
        Mapper(name, port), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    name = sys.argv[1]
    port = sys.argv[2]
    # print(name, port)
    main(name, port)
