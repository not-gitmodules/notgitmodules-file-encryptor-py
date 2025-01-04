from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from typing import Union, List, Set, Tuple
from .salt import Salt
from .protocols import BinaryFileManager

FilesToEncodeType = Union[List[str], Set[str], Tuple[str]]


class FileEncryptor:

    def __init__(
        self,
        binary_file_manager: BinaryFileManager,
        files_to_encode: FilesToEncodeType,
        use_salt: bool = False,
        save_salt: bool = True,
        salt_file_name='salt',
        delete_original_file: bool = False
    ):
        """
        :param binary_file_manager: the file manager class for binary files
        :param save_salt: Save salt to a file?
        :param salt_file_name: according to how the salt file is named in your project
        :param delete_original_file: delete the original file after encryption/decryption. Recommended to set to False in development and True in production.
        :param use_salt: use salt for encryption?
        - files_to_encode: raw filenames, do not include .enc
        - true: it adds salt that will be saved in a file
        - false: it doesn't add salt, and encrypts using the master key given


        """
        self.files_to_encode: FilesToEncodeType = files_to_encode
        self.binary_file_manager: BinaryFileManager = binary_file_manager
        self.delete_original_file: bool = delete_original_file

        _master_key = bytes(input("Enter the key: "), 'utf-8')

        if use_salt:
            salt_obj = Salt(
                binary_file_manager=binary_file_manager,
                save_salt=save_salt,
                salt_file_name=salt_file_name
            )
            salt = salt_obj.initialize_salt()

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=480000,
            )

            key = base64.urlsafe_b64encode(kdf.derive(_master_key))
            self._fernet = Fernet(key)
        else:
            key = base64.urlsafe_b64encode(_master_key.ljust(32)[:32])
            self._fernet = Fernet(key)

    def encrypt(self):
        for file_name in self.files_to_encode:
            if os.path.exists(file_name):
                file_data: bytes = self.binary_file_manager.read(file_name)
                encrypted_data: bytes = self._fernet.encrypt(file_data)
                self.binary_file_manager.write(file_path=f"{file_name}.enc", content=encrypted_data)
                # delete the original file
                if self.delete_original_file:
                    self.binary_file_manager.delete(file_name)

    def decrypt(self):
        for file_name in self.files_to_encode:
            file_name_enc = file_name + ".enc"
            if os.path.exists(file_name_enc):
                encrypted_data: bytes = self.binary_file_manager.read(file_name_enc)
                try:
                    data = self._fernet.decrypt(encrypted_data)
                except InvalidToken:
                    raise ValueError("Key does not match or the file has been tampered with.")
                else:
                    self.binary_file_manager.write(file_path=file_name, content=data)
                    # delete the original encrypted file
                    if self.delete_original_file:
                        self.binary_file_manager.delete(file_name_enc)
            else:
                raise FileNotFoundError(os.path.abspath(file_name_enc), 'was not found')
