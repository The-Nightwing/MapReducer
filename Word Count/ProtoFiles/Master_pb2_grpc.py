# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import Master_pb2 as Master__pb2


class MasterServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.MasterMap = channel.unary_unary(
                '/rpc.MasterService/MasterMap',
                request_serializer=Master__pb2.Request.SerializeToString,
                response_deserializer=Master__pb2.Response.FromString,
                )
        self.MasterReducer = channel.unary_unary(
                '/rpc.MasterService/MasterReducer',
                request_serializer=Master__pb2.Request.SerializeToString,
                response_deserializer=Master__pb2.Response.FromString,
                )


class MasterServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def MasterMap(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MasterReducer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MasterServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'MasterMap': grpc.unary_unary_rpc_method_handler(
                    servicer.MasterMap,
                    request_deserializer=Master__pb2.Request.FromString,
                    response_serializer=Master__pb2.Response.SerializeToString,
            ),
            'MasterReducer': grpc.unary_unary_rpc_method_handler(
                    servicer.MasterReducer,
                    request_deserializer=Master__pb2.Request.FromString,
                    response_serializer=Master__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'rpc.MasterService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MasterService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def MasterMap(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.MasterService/MasterMap',
            Master__pb2.Request.SerializeToString,
            Master__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def MasterReducer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/rpc.MasterService/MasterReducer',
            Master__pb2.Request.SerializeToString,
            Master__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
