from models.database import Database
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class Licitacion:
    def __init__(self):
        self.db = Database()
        self.api_url = "https://api.mercadopublico.cl/servicios/v1/publico/licitaciones.json"
        self.api_ticket = os.getenv("API_TICKET", "t0C31C2BA-3AE1-4F07-9124-F12E946BE6E3")

    def obtener_licitaciones_api(self, fecha=None):
        try:
            headers = {"Accept": "application/json"}
            params = {"ticket": self.api_ticket}
            if fecha:
                params["fecha"] = fecha
            response = requests.get(self.api_url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json().get("Listado", [])
            print(f"API response: {data}")  # Depuración
            return data
        except requests.RequestException as e:
            print(f"Error al obtener licitaciones: {e}")
            return []

    def guardar_licitaciones(self, licitaciones):
        query = """
        INSERT INTO licitaciones (codigo, nombre, descripcion, fecha_cierre)
        VALUES (%s, %s, %s, %s)
        """
        for lic in licitaciones:
            params = (
                lic.get("CodigoExterno", ""),
                lic.get("Nombre", ""),
                lic.get("Descripcion", ""),
                lic.get("FechaCierre", None)
            )
            self.db.execute_query(query, params)

    def actualizar(self, id, codigo, nombre, descripcion, fecha_cierre):
        query = """
        UPDATE licitaciones
        SET codigo = %s, nombre = %s, descripcion = %s, fecha_cierre = %s
        WHERE id = %s
        """
        self.db.execute_query(query, (codigo, nombre, descripcion, fecha_cierre, id))

    def eliminar(self, id):
        query = "DELETE FROM licitaciones WHERE id = %s"
        self.db.execute_query(query, (id,))

    def cerrar_conexion(self):
        self.db.close()