import os
import hashlib


class AuthenticationTokenVerifier:

    def __init__(self, file_name: str):
        self.file_name = file_name

    def read_data(self):
        try:
            with open(self.file_name) as data:
                data = data.readline().split("=")[1]
            return data, None
        except FileNotFoundError as error:
            return None, error

    def create_file(self, security_string: str = "."):
        if not os.path.exists(f"./{self.file_name}"):
            token = hashlib.sha256(security_string.encode("utf-8")).hexdigest()
            try:
                file = open(self.file_name, 'w+')
                file.write(f"token={token}")
                return token
            except FileNotFoundError as error:
                return "error"
        return "exists"
