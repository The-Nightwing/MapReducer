from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MapperRequest(_message.Message):
    __slots__ = ["filenames", "reducers"]
    FILENAMES_FIELD_NUMBER: _ClassVar[int]
    REDUCERS_FIELD_NUMBER: _ClassVar[int]
    filenames: _containers.RepeatedScalarFieldContainer[str]
    reducers: int
    def __init__(self, reducers: _Optional[int] = ..., filenames: _Optional[_Iterable[str]] = ...) -> None: ...

class MapperResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...
