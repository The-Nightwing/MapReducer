import grpc
import master_pb2 as master_pb2
import master_pb2_grpc as master_pb2_grpc

if __name__ == '__main__':
    with grpc.insecure_channel('localhost:8888') as channel:
        stub = master_pb2_grpc.MasterStub(channel)
        response = stub.worker(master_pb2.ClientRequest())