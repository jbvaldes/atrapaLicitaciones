from flask import Flask, render_template, request, redirect, url_for, flash, session
from controllers.auth_controller import AuthController
from controllers.licitacion_controller import LicitacionController

app = Flask(__name__)
app.secret_key = 'una_clave_secreta_muy_larga_y_aleatoria'

auth_controller = AuthController()
licitacion_controller = LicitacionController()

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('licitaciones'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_controller.login(username, password):
            session['logged_in'] = True
            session['username'] = username
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('licitaciones'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_controller.registrar(username, password):
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error al registrar usuario.', 'danger')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))

@app.route('/licitaciones')
def licitaciones():
    if 'logged_in' not in session:
        flash('Por favor, inicia sesión.', 'warning')
        return redirect(url_for('login'))
    page = request.args.get('page', 1, type=int)
    fecha_ingresada = request.args.get('fecha', '')
    per_page = 10
    licitaciones, total = licitacion_controller.listar(page, per_page)
    total_pages = (total + per_page - 1) // per_page
    # Depuración: Imprimir número de licitaciones
    print(f"Número de licitaciones: {len(licitaciones)}")
    return render_template('licitaciones.html', licitaciones=licitaciones, current_page=page, total_pages=total_pages, fecha_ingresada=fecha_ingresada)

@app.route('/obtener_licitaciones', methods=['POST'])
def obtener_licitaciones():
    if 'logged_in' not in session:
        flash('Por favor, inicia sesión.', 'warning')
        return redirect(url_for('login'))
    fecha = request.form['fecha']
    formatted_fecha = None
    if fecha:
        try:
            day, month, year = fecha.split('/')
            formatted_fecha = f"{day.zfill(2)}{month.zfill(2)}{year}"
        except ValueError:
            flash('Formato de fecha inválido. Use DD/MM/AAAA.', 'danger')
            return redirect(url_for('licitaciones', fecha=fecha))
    if licitacion_controller.obtener_y_guardar_licitaciones(formatted_fecha):
        flash('Licitaciones guardadas exitosamente.', 'success')
    else:
        flash('Error al obtener licitaciones. Verifica el ticket o la conexión.', 'danger')
    return redirect(url_for('licitaciones', fecha=fecha))

@app.route('/licitaciones/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar_licitacion(id):
    if 'logged_in' not in session:
        flash('Por favor, inicia sesión.', 'warning')
        return redirect(url_for('login'))
    # Obtener todas las licitaciones para buscar la correcta
    licitaciones, _ = licitacion_controller.listar(page=1, per_page=1000)  # Obtener suficientes registros
    licitacion = next((lic for lic in licitaciones if lic['id'] == id), None)
    if not licitacion:
        flash('Licitación no encontrada.', 'danger')
        return redirect(url_for('licitaciones'))
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        fecha_cierre = request.form['fecha_cierre']
        if not codigo or not nombre:
            flash('Código y Nombre son obligatorios.', 'danger')
            return redirect(url_for('actualizar_licitacion', id=id))
        licitacion_controller.actualizar(id, codigo, nombre, descripcion, fecha_cierre)
        flash('Licitación actualizada exitosamente.', 'success')
        return redirect(url_for('licitaciones'))
    return render_template('actualizar_licitacion.html', licitacion=licitacion)

@app.route('/licitaciones/eliminar/<int:id>', methods=['POST'])
def eliminar_licitacion(id):
    if 'logged_in' not in session:
        flash('Por favor, inicia sesión.', 'warning')
        return redirect(url_for('login'))
    licitacion_controller.eliminar(id)
    flash('Licitación eliminada exitosamente.', 'success')
    return redirect(url_for('licitaciones'))

if __name__ == '__main__':
    app.run(debug=True)