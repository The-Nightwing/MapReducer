from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Request(_message.Message):
    __slots__ = ["index"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    index: str
    def __init__(self, index: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
