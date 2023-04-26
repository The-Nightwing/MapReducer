from concurrent import futures
import grpc
import master_pb2 as master_pb2
import master_pb2_grpc as master_pb2_grpc
import mapper_pb2 as mapper_pb2
import mapper_pb2_grpc as mapper_pb2_grpc
import multiprocessing
import threading
import os


class Master(master_pb2_grpc.MasterServicer):
    def __init__(self, inputLocation, outputLocation, M, R):
        super().__init__()
        self.inputLocation = inputLocation
        self.outputLocation = outputLocation
        self.M = M
        self.R = R

        # start M processes and open mapper.py
        # start R processes and open reducer.py
        self.spawnMappers()
        self.spawnReducers()

    def mapFilesToMappers(self):
        files = os.listdir(self.inputLocation)
        self.filesPerMapper = [[] for i in range(self.M)]
        for i in range(len(files)):
            self.filesPerMapper[i % self.M].append(self.inputLocation + files[i])

    def worker(self, request, context):
        self.mapFilesToMappers()
        threads = []

        for i in range(self.M):
            thread = threading.Thread(target=self.startMapping(i))
            thread.start()
            threads.append(thread)

    def startReduce(self):
        for i in range(self.R):
            with grpc.insecure_channel('localhost:'+str(6000+self.M+i)) as channel:
                stub = mapper_pb2_grpc.ReducerStub(channel)
                response = stub.reduce(mapper_pb2.ReducerRequest(outputLocation=self.outputLocation, index = i, count_M = self.M))
        
    def startMapping(self, index):
        with grpc.insecure_channel('localhost:'+str(6000+index)) as channel:
            stub = mapper_pb2_grpc.MapperStub(channel)
            response = stub.map(mapper_pb2.MapperRequest(
                reducers=self.R, filenames=self.filesPerMapper[index], outputLocation = self.outputLocation))
        
    def spawnReducers(self):
        self.spawnReducers = []
        print("spawned Reducers")
        for i in range(self.R):
            name = i+1
            port = 6000+self.M+i
            process = multiprocessing.Process(
                target=os.system, args=(f'python reducer.py {name} {port}',))
            self.spawnReducers.append(process)
            process.start()

    def spawnMappers(self):
        self.spawnedMappers = []
        print("spawned Mappers")
        for i in range(self.M):
            name = i+1
            port = 6000+i
            process = multiprocessing.Process(
                target=os.system, args=(f'python mapper.py {name} {port}',))
            self.spawnedMappers.append(process)
            process.start()

    def mapperFinished(self, request, context):
        self.mapperFinishCounter+=1
        if self.mapperFinishCounter == self.M:
            self.startReduce()

import sys

def start(inputLocation, outputLocation, M, R):
    port = '8888'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    master_pb2_grpc.add_MasterServicer_to_server(
        Master(inputLocation, outputLocation, M, R), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    configFile = "D:\DSCD PROJECT\MapReducer\Word Count\config.txt"
    # configFile = sys.argv[1]
    with open(configFile, 'r') as config:
        lines = config.readlines()
        inputLocation = lines[0].strip()
        outputLocation = lines[1].strip()
        M = int(lines[2].strip())
        R = int(lines[3].strip())
        # print(M, R, outputLocation, inputLocation)
    start(inputLocation, outputLocation, M, R)



# python -m grpc_tools.protoc -I./  --python_out=./ ./master.proto --pyi_out=./ --grpc_python_out=./
