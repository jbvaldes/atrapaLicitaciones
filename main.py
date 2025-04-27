import tkinter as tk
from views.auth_view import AuthView

def main():
    root = tk.Tk()
    app = AuthView(root)
    root.mainloop()

if __name__ == "__main__":
    main()