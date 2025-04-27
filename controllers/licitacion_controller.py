from models.licitacion import Licitacion

class LicitacionController:
    def __init__(self):
        self.model = Licitacion()

    def obtener_y_guardar_licitaciones(self, fecha=None):
        licitaciones = self.model.obtener_licitaciones_api(fecha)
        if licitaciones:
            self.model.guardar_licitaciones(licitaciones)
            return True
        return False

    def listar(self, page=1, per_page=10):
        offset = (page - 1) * per_page
        query = "SELECT * FROM licitaciones LIMIT %s OFFSET %s"
        licitaciones = self.model.db.fetch_query(query, (per_page, offset))
        total_query = "SELECT COUNT(*) as total FROM licitaciones"
        total_result = self.model.db.fetch_query(total_query)
        total = total_result[0]['total'] if total_result else 0
        # Depuración: Imprimir estructura de licitaciones
        print(f"Licitaciones devueltas: {licitaciones}")
        return licitaciones, total

    def actualizar(self, id, codigo, nombre, descripcion, fecha_cierre):
        self.model.actualizar(id, codigo, nombre, descripcion, fecha_cierre)

    def eliminar(self, id):
        self.model.eliminar(id)