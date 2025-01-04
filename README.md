# Python file encryptor Gitmodule

--- 
## About

This encryptor provides two options of encryption:
- **(with salt)** generate salt based on the key provided by you, then encrypt files using that salt
- **(without salt)** encrypt files using your key

It optionally provides an option (if salt is used):
- to save the salt to a file

---
## Technical Overview of `FileEncryptor`

`FileEncryptor` is a class designed to handle the encryption and decryption of files using symmetric encryption (Fernet). It uses the `cryptography` library for encryption and key derivation, with support for both salt-based and master key-based encryption.

#### Key Features:
1. **Encryption Mechanism**:
    - Uses the `cryptography.fernet.Fernet` class for AES encryption.
    - For key generation, it supports two modes:
        - **With Salt**: Derives the key using PBKDF2-HMAC with SHA-256 and a salt.
        - **Without Salt**: Uses a master key directly, truncated/padded to 32 bytes.

2. **Modes**:
    - **Encrypt**: Reads files, encrypts them using the derived or provided key, and stores the encrypted data with a `.enc` extension. The original file is deleted after encryption.
    - **Decrypt**: Decrypts files with the `.enc` extension using the stored key, restores the original file, and deletes the encrypted file.

#### Key Operations:
- **Encryption**: Generates a secure key (either from PBKDF2 with salt or a provided master key) and encrypts the file's content.
- **Decryption**: Decrypts files using the same key and restores the original content.

#### Dependencies:
- **`cryptography.fernet.Fernet`** for encryption.
- **PBKDF2-HMAC** for key derivation when using salt.
- **`BinaryFileManager`** interface for file handling (read/write/delete).

---
# Usage

---
- ### Usage with `not_gitmodules` (recommended) 

   - [What's not_gimodules](https://github.com/Armen-Jean-Andreasian/not_gitmodules.git) ?



1. First of all, this module requires another module: `FileManager`

Open `not_gitmodules.yaml` file and add it, alongside with this module, example:

```yaml
file_manager : https://github.com/Armen-Jean-Andreasian/notgitmodules-file-manager
file_encryptor : https://github.com/Armen-Jean-Andreasian/notgitmodules-file-encryptor-py
```


2. Update Not Gitmodules, example:

```bash
pip install -r from my_gitmodules/requirements.txt
```


3. Install the library dependencies

```bash
pip install -r from my_gitmodules.requirements.txt
```

or manually include

`cryptography~=44.0.0` to your `requirements.txt`

---

- ### Usage with `gitmodules`

For `gitmodules`, follow the usual steps to add the repository as a submodule to your project and use it as needed.

---

3. Initialize `FileManager` class and pass it to `FileEncryptor`

```python
from my_gitmodules.file_encryptor import FileEncryptor
from my_gitmodules.file_manager_module import BinaryFileManager

bin_manager = BinaryFileManager()

file_encryptor = FileEncryptor(
    binary_file_manager=bin_manager,
    files_to_encode=[
        '.env', 'some_file.txt'
    ],
    use_salt=True,
    save_salt=True,
    salt_file_name='playground/salt',
    delete_original_file=False
)

file_encryptor.encrypt() # to encrypt file(s)
file_encryptor.decrypt() # to decrypt file(s)
```
---


## Docker: Important note

You need to provide the key through `input()` function, so the Docker container should be run interactively (i.e., with the `-it` flag).

_The `-it` flag ensures that the container is interactive and connected to the terminal, allowing the user to provide input directly._

Here’s a scenario:

### 1. Dockerfile Example

```Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "file.py"]
```

### 2. docker-compose.yml Example

```yaml
version: '3'
services:
  myapp:
    build: .
    stdin_open: true
    tty: true
```

### 3. Running the Container

With the `-it` flag, you can run the container interactively:

```bash
docker run -it myapp
```

Or, if using Docker Compose:

```bash
docker-compose run myapp
```

---

## Some examples

```python
from my_gitmodules.file_encryptor import FileEncryptor
from my_gitmodules.file_manager_module import BinaryFileManager

bin_manager = BinaryFileManager()


def encryptor_with_salt():
    return FileEncryptor(
        binary_file_manager=bin_manager,
        files_to_encode=[
            'file1.txt',
        ],
        use_salt=True,
        save_salt=True,
        salt_file_name='salt'
    )


def encryptor_without_salt():
    return FileEncryptor(
        binary_file_manager=bin_manager,
        files_to_encode=[
            'file2.txt',
        ],
        use_salt=True,
        save_salt=True,
        salt_file_name='salt'
    )


s_encryptor = encryptor_with_salt()

s_encryptor.encrypt()
s_encryptor.decrypt()

encryptor = encryptor_without_salt()
encryptor.encrypt()
encryptor.decrypt()
```