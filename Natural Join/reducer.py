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
        # f = open('ouuuu.txt', 'w')
        # f.write('hehe')
        keys = dict()
        print(index)
        self.commonKey = ''
        self.key1 = ''
        self.key2 = ''
        for j in range(self.count_M):
            with open(self.outputLocation + 'M' + str(j+1) +'_P'+str(index)+'.txt', 'r') as f:
                lines = f.readlines()
                print(lines)
                for line in lines:
                    print(line)
                    key, value = line.strip().split('#')
                    value = eval(value)
                    print(key)
                    if key in keys:
                        keys[key][value[0]].append(value[1])
                    else:
                        keys[key] = {1:[],2:[]}
                        keys[key][value[0]].append(value[1])
                    self.commonKey = value[2]
                    if value[0]==1:
                        self.key1 = value[3]
                    if value[0]==2:
                        self.key2 = value[3]
        # sort keyValues
        print("Writing stuff")
        with open(self.outputLocation + 'output_'+ str(self.name)+'.txt', 'w') as f:
            print(keys.items())
            f.write(str(self.commonKey) + ',' +self.key1+','+self.key2+'\n')
            for key, value in keys.items():
                for t1v in value[1]:
                    for t2v in value[2]:
                        f.write(str(key)+','+str(t1v)+','+str(t2v)+'\n')

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
