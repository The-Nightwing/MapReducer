from concurrent import futures
import grpc
import ProtoFiles.master_pb2 as Master_pb2
import ProtoFiles.master_pb2_grpc as Master_pb2_grpc
import ProtoFiles.mapper_pb2 as mapper_pb2
import ProtoFiles.mapper_pb2_grpc as mapper_pb2_grpc
import multiprocessing
import threading
import os

class Master(Master_pb2_grpc.MasterServicer):
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
        self.filesPerMapper = [files[i::self.M] for i in range(self.M)]
        
    
    def worker(self, request, context):
        self.mapFilesToMappers()
        for i in range(self.M):
            thread = threading.Thread(target=self.startMapping(i))
            thread.start()
            
    def startMapping(self, index):
        with grpc.insecure_channel('localhost:'+str(6000+index)) as channel:
            stub = mapper_pb2_grpc.MapperStub(channel)
            response = stub.map(mapper_pb2.MapperRequest(reducers = self.R, filenames = self.filesPerMapper[0]))
            print(response.status)

    def spawnReducers(self):
        self.spawnReducers = []
        for i in range(self.R):
            name = i+1
            port = 6000+self.M+i
            process = multiprocessing.Process(target=os.system, args=(f'python reducer.py {name} {port}'))
            self.spawnReducers.append(process)
            process.start()

    def spawnMappers(self):
        self.spawnedMappers = []
        for i in range(self.M):
            name = i+1
            port = 6000+i
            process = multiprocessing.Process(target=os.system, args=(f'python mapper.py {name} {port}'))
            self.spawnedMappers.append(process)
            process.start()
    
    def mapperFinished(self, request, context):
        print(request.status)

    def reducerFinished(self, request, context):
        print(request.status)


def start():
    inputLocation = input("Input Location: ")
    outputLocation = input("Output Location: ")
    M = int(input("Number of Mappers: "))
    R = int(input("Number of Reducers: "))

    port = '8888'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Master_pb2_grpc.add_MasterServiceServicer_to_server(Master(inputLocation, outputLocation, M, R), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    server.wait_for_termination()
    
if __name__ == "__main__":
    start()


# python -m grpc_tools.protoc -I./  --python_out=ProtoFiles/ ./Master.proto --pyi_out=ProtoFiles/ --grpc_python_out=ProtoFiles/