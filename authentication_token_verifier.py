class AuthenticationTokenVerifier:

    def __init__(self, file_name: str):
        self.file_name = file_name

    def read_data(self):
        try:
            with open(self.file_name) as data:
                data = data.readline().split("=")[1]
            return None, data
        except FileNotFoundError as error:
            return error, None

    def create_file(self):
        try:
            file = open(self.file_name, 'w+')
            return None, "File created"
        except FileNotFoundError as error:
            return error, None
