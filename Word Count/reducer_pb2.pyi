from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReducerRequest(_message.Message):
    __slots__ = ["count_M", "index", "outputLocation"]
    COUNT_M_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    OUTPUTLOCATION_FIELD_NUMBER: _ClassVar[int]
    count_M: int
    index: int
    outputLocation: str
    def __init__(self, outputLocation: _Optional[str] = ..., index: _Optional[int] = ..., count_M: _Optional[int] = ...) -> None: ...

class ReducerResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
