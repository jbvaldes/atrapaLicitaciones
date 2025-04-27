from models.usuario import Usuario

class AuthController:
    def __init__(self):
        self.model = Usuario()

    def registrar(self, username, password):
        return self.model.registrar(username, password)

    def login(self, username, password):
        return self.model.login(username, password)