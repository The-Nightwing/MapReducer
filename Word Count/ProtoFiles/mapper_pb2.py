# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mapper.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cmapper.proto\x12\x03rpc\"4\n\rMapperRequest\x12\x10\n\x08reducers\x18\x01 \x01(\x05\x12\x11\n\tfilenames\x18\x02 \x03(\t\" \n\x0eMapperResponse\x12\x0e\n\x06status\x18\x01 \x01(\t2A\n\rMapperService\x12\x30\n\x03map\x12\x12.rpc.MapperRequest\x1a\x13.rpc.MapperResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mapper_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MAPPERREQUEST._serialized_start=21
  _MAPPERREQUEST._serialized_end=73
  _MAPPERRESPONSE._serialized_start=75
  _MAPPERRESPONSE._serialized_end=107
  _MAPPERSERVICE._serialized_start=109
  _MAPPERSERVICE._serialized_end=174
# @@protoc_insertion_point(module_scope)
