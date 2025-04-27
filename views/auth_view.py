import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import AuthController
from views.licitacion_view import LicitacionView

class AuthView:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Licitaciones - Login")
        self.root.geometry("400x300")
        self.controller = AuthController()
        self.create_login_window()

    def create_login_window(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título
        tk.Label(self.root, text="Iniciar Sesión", font=("Arial", 16)).pack(pady=20)

        # Frame para entradas
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Entrada de usuario
        tk.Label(frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Entrada de contraseña
        tk.Label(frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botones
        tk.Button(self.root, text="Iniciar Sesión", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Registrarse", command=self.create_register_window).pack(pady=5)

    def create_register_window(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()

        # Título
        tk.Label(self.root, text="Registrarse", font=("Arial", 16)).pack(pady=20)

        # Frame para entradas
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Entrada de usuario
        tk.Label(frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.reg_username_entry = tk.Entry(frame)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5)

        # Entrada de contraseña
        tk.Label(frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.reg_password_entry = tk.Entry(frame, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Botones
        tk.Button(self.root, text="Registrar", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Volver", command=self.create_login_window).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        if self.controller.login(username, password):
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")
            self.root.destroy()  # Cerrar ventana de login
            root = tk.Tk()  # Crear nueva ventana para licitaciones
            app = LicitacionView(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return
        if self.controller.registrar(username, password):
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            self.create_login_window()
        else:
            messagebox.showerror("Error", "Error al registrar usuario.")
