# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: reducer.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rreducer.proto\x12\x03rpc\"\x10\n\x0eReducerRequest\"!\n\x0fReducerResponse\x12\x0e\n\x06status\x18\x01 \x01(\t2E\n\x0eReducerService\x12\x33\n\x06reduce\x12\x13.rpc.ReducerRequest\x1a\x14.rpc.ReducerResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'reducer_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REDUCERREQUEST._serialized_start=22
  _REDUCERREQUEST._serialized_end=38
  _REDUCERRESPONSE._serialized_start=40
  _REDUCERRESPONSE._serialized_end=73
  _REDUCERSERVICE._serialized_start=75
  _REDUCERSERVICE._serialized_end=144
# @@protoc_insertion_point(module_scope)
