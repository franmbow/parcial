from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Datos

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basedatos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'clave_secreta'

db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['usuario']
        password = request.form['clave']
        user = Usuario.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['usuario'] = username
            return redirect(url_for('formulario'))
        else:
            return render_template('index.html', error="Credenciales incorrectas")
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        nuevo = Datos()

        # ID ya queda autogenerado
        # TODO: completar el resto de los campos a partir del modelo
        nombre = request.form['nombre']
        edad = request.form['edad']
        email = request.form['email']
        ciudad = request.form['ciudad']
        nuevo.nombre = nombre
        nuevo.edad = edad
        nuevo.email = email
        nuevo.ciudad = ciudad
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for('listado'))
    return render_template('formulario.html')

@app.route('/listado')
def listado():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    datos = Datos.query.all()
    return render_template('listado.html', datos=datos)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    dato = Datos.query.get_or_404(id)
    if request.method == 'POST':
        
        # TODO: Asignar valores desde request.form
        # Ejemplo: dato.nombre = request.form['nombre']
        dato.nombre = request.form['nombre']
        dato.edad = request.form['edad']
        dato.email = request.form['email']
        dato.ciudad = request.form['ciudad']
        db.session.commit()
        return redirect(url_for('listado'))
    return render_template('formulario.html', dato=dato)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))
    dato = Datos.query.get_or_404(id)
    db.session.delete(dato)
    db.session.commit()
    # TODO: completar el resto del codigo para que se borre el registro
    
    return redirect(url_for('listado'))

# TODO: Agregar una nueva ruta /acerca para mostrar el html acerca.html
@app.route('/acerca')
def acerca():
    return render_template('acerca.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Usuario.query.filter_by(username='politecnico').first():
            nuevo = Usuario(username='politecnico', password=generate_password_hash('malvinas'))
            db.session.add(nuevo)
            db.session.commit()
        
        if not Usuario.query.filter_by(username='Abdala').first():
            nuevo = Usuario(username='Abdala', password=generate_password_hash('1234'))
            db.session.add(nuevo)
            db.session.commit()
    app.run(debug=True)
