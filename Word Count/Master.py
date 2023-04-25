from concurrent import futures
import grpc
import ProtoFiles.Master_pb2 as Master_pb2
import ProtoFiles.Master_pb2_grpc as Master_pb2_grpc


class Master(Master_pb2_grpc.MasterServiceServicer):
    def __init__(self, inputLocation, outputLocation, M, R):
        super().__init__()
        self.inputLocation = inputLocation
        self.outputLocation = outputLocation
        self.M = M
        self.R = R
    
    def MasterMap(self, request, context):
        print("MasterMap: " + request.index)
        return Master_pb2.Response(Master_pb2.Response())
    
    def MasterReducer(self, request, context):
        print("MasterReducer: " + request.index)
        return Master_pb2.Response(Master_pb2.Response())
    
    def WordCount():
        pass
    

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