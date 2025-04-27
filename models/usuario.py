from models.database import Database
import hashlib
from models.database import Database
import hashlib

class Usuario:
    def __init__(self):
        self.db = Database()

    def registrar(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = "INSERT INTO usuarios (username, password) VALUES (%s, %s)"
        self.db.execute_query(query, (username, hashed_password))
        return True

    def login(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
        result = self.db.fetch_query(query, (username, hashed_password))
        return len(result) > 0

    def cerrar_conexion(self):
        self.db.close()