
import tkinter as tk
from tkinter import messagebox, ttk
from controllers.licitacion_controller import LicitacionController

class LicitacionView:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Licitaciones")
        self.root.geometry("800x600")
        self.controller = LicitacionController()
        self.create_main_window()

    def create_main_window(self):
        # Título
        tk.Label(self.root, text="Gestión de Licitaciones", font=("Arial", 16)).pack(pady=10)

        # Frame para acciones
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)

        # Campo para ticket de API
        tk.Label(action_frame, text="Ticket API:").grid(row=0, column=0, padx=5)
        self.ticket_entry = tk.Entry(action_frame)
        self.ticket_entry.grid(row=0, column=1, padx=5)

        # Botón para obtener licitaciones
        tk.Button(action_frame, text="Obtener Licitaciones", command=self.obtener_licitaciones).grid(row=0, column=2, padx=5)

        # Botones CRUD
        tk.Button(action_frame, text="Actualizar Licitación", command=self.abrir_ventana_actualizar).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(action_frame, text="Eliminar Licitación", command=self.eliminar_licitacion).grid(row=1, column=1, padx=5, pady=5)

        # Tabla para mostrar licitaciones
        self.tree = ttk.Treeview(self.root, columns=("ID", "Código", "Nombre", "Descripción", "Fecha Cierre"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Fecha Cierre", text="Fecha Cierre")
        self.tree.column("ID", width=50)
        self.tree.column("Código", width=100)
        self.tree.column("Nombre", width=200)
        self.tree.column("Descripción", width=300)
        self.tree.column("Fecha Cierre", width=150)
        self.tree.pack(pady=10, fill="both", expand=True)

        # Botón para salir
        tk.Button(self.root, text="Salir", command=self.root.destroy).pack(pady=10)

        # Cargar licitaciones iniciales
        self.listar_licitaciones()

    def obtener_licitaciones(self):
        ticket = self.ticket_entry.get()
        if not ticket:
            messagebox.showerror("Error", "Por favor, ingrese un ticket válido.")
            return
        if self.controller.obtener_y_guardar_licitaciones(ticket):
            messagebox.showinfo("Éxito", "Licitaciones guardadas exitosamente.")
            self.listar_licitaciones()
        else:
            messagebox.showerror("Error", "Error al obtener licitaciones.")

    def listar_licitaciones(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Obtener licitaciones
        licitaciones = self.controller.listar()
        for lic in licitaciones:
            self.tree.insert("", "end", values=(
                lic["id"],
                lic["codigo"],
                lic["nombre"],
                lic["descripcion"],
                lic["fecha_cierre"]
            ))

    def abrir_ventana_actualizar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una licitación para actualizar.")
            return

        licitacion = self.tree.item(selected_item)["values"]
        self.ventana_actualizar = tk.Toplevel(self.root)
        self.ventana_actualizar.title("Actualizar Licitación")
        self.ventana_actualizar.geometry("400x300")

        # Frame para entradas
        frame = tk.Frame(self.ventana_actualizar)
        frame.pack(pady=10)

        # Entradas
        tk.Label(frame, text="Código:").grid(row=0, column=0, padx=5, pady=5)
        self.update_codigo_entry = tk.Entry(frame)
        self.update_codigo_entry.grid(row=0, column=1, padx=5, pady=5)
        self.update_codigo_entry.insert(0, licitacion[1])

        tk.Label(frame, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        self.update_nombre_entry = tk.Entry(frame)
        self.update_nombre_entry.grid(row=1, column=1, padx=5, pady=5)
        self.update_nombre_entry.insert(0, licitacion[2])

        tk.Label(frame, text="Descripción:").grid(row=2, column=0, padx=5, pady=5)
        self.update_descripcion_entry = tk.Entry(frame)
        self.update_descripcion_entry.grid(row=2, column=1, padx=5, pady=5)
        self.update_descripcion_entry.insert(0, licitacion[3])

        tk.Label(frame, text="Fecha Cierre (YYYY-MM-DD HH:MM:SS):").grid(row=3, column=0, padx=5, pady=5)
        self.update_fecha_entry = tk.Entry(frame)
        self.update_fecha_entry.grid(row=3, column=1, padx=5, pady=5)
        self.update_fecha_entry.insert(0, licitacion[4] if licitacion[4] else "")

        # Botón para guardar cambios
        tk.Button(self.ventana_actualizar, text="Guardar", command=lambda: self.actualizar_licitacion(licitacion[0])).pack(pady=10)

    def actualizar_licitacion(self, id):
        codigo = self.update_codigo_entry.get()
        nombre = self.update_nombre_entry.get()
        descripcion = self.update_descripcion_entry.get()
        fecha_cierre = self.update_fecha_entry.get()

        if not codigo or not nombre:
            messagebox.showerror("Error", "Código y Nombre son obligatorios.")
            return

        self.controller.actualizar(id, codigo, nombre, descripcion, fecha_cierre)
        messagebox.showinfo("Éxito", "Licitación actualizada.")
        self.ventana_actualizar.destroy()
        self.listar_licitaciones()

    def eliminar_licitacion(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una licitación para eliminar.")
            return

        licitacion_id = self.tree.item(selected_item)["values"][0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta licitación?"):
            self.controller.eliminar(licitacion_id)
            messagebox.showinfo("Éxito", "Licitación eliminada.")
            self.listar_licitaciones()