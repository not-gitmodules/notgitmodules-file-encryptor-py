import os
from .protocols import BinaryFileManager


class Salt:
    def __init__(
        self,
        binary_file_manager: BinaryFileManager,
        save_salt: bool,
        salt_file_name: str,

    ):
        self.binary_file_manager = binary_file_manager
        self.save_salt = save_salt
        self.salt_file_name = salt_file_name

    def initialize_salt(self) -> bytes:
        try:
            # reading file
            salt = self.binary_file_manager.read(self.salt_file_name)
        except FileNotFoundError:
            # if salt file not found -> generating and saving
            salt = self.__generate_new_salt()
        else:
            # if file found
            if not salt:  # but salt is empty -> generating and saving
                salt = self.__generate_new_salt()
        return salt


    def __generate_new_salt(self) -> bytes:
        salt: bytes = os.urandom(16)
        if self.save_salt:
            self.binary_file_manager.write(file_path=self.salt_file_name, content=salt)
        return salt
