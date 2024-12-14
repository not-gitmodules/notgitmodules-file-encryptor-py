from typing import Protocol


class BinaryFileManager(Protocol):
    def read(self, file_path: str) -> bytes:
        ...

    def write(self, file_path: str, content: bytes) -> None:
        ...

    def append(self, file_path: str, content: bytes) -> None:
        ...

    def exclusive_append(self, file_path: str, content: bytes) -> None:
        ...

    def delete(self, file_path: str) -> None:
        ...

    def move(self, file_path: str, destination: str) -> None:
        ...
