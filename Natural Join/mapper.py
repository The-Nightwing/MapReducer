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
        commonKey = self.findCommonKey(filenames)
        self.outputLocation = request.outputLocation
        print(f'MAPPER is here name {self.name}')
        keyVPairs = []
        for filename in filenames:
            with open(filename, 'r') as f:
                table = 1 if filename.endswith('1.txt') else 2
                keys = f.readline().strip().split(',')
                commonKeyIndex = 0 if commonKey==keys[0] else 1
                otherIndex = 1 if commonKeyIndex==0 else 0
                rows = f.readlines()
                for row in rows:
                    arow = row.strip().split(',')
                    keyVPairs.append((arow[commonKeyIndex], (table, arow[otherIndex], commonKey, keys[otherIndex])))

        self.partitionStrategy(keyVPairs)
        self.notifyMaster()
        print(f'MAPPER is leaving name {self.name}')
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
    
    def findCommonKey(self, filenames):
        table1 = ""
        table2 = ""
        for filename in filenames:
            if filename.endswith("table1.txt"):
                table1 = filename
        for filename in filenames:
            if filename.endswith("table2.txt"):
                table2 = filename
        keys1 = []
        keys2 = []
        with open(table1, "r") as t1:
            keys1 = t1.readline().strip().split(',')
        with open(table2, "r") as t2:
            keys2 = t2.readline().strip().split(',')
        if keys1[0] in keys2:
            return keys1[0]
        else:
            return keys1[1]

            
    
    def partitionStrategy(self, keyVPairs):
        
            for tuple in keyVPairs:
                #Hash function
                hash_ = self.HashFunction(tuple[0], self.reducers)
                reducer = hash_
                with open(self.outputLocation +'M'+str(self.name) +'_P'+str(reducer)+'.txt', 'a') as f:
                    f.write(str(tuple[0]) + '#' + str(tuple[1]) + '\n')

def main(name, port):
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
