from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__, template_folder='templates')

# Carpeta para imágenes temporales
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/temp')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Clave secreta
app.config['SECRET_KEY'] = os.urandom(24)

# Conexión a PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuariosgamers_user:ogeJ1nFI1aAu3iv6cOrDEcFoNbkziUeV@dpg-cvusba3e5dus73e0idp0-a/usuariosgamers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)

# Modelo de usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    pais = db.Column(db.String(50))
    imagen = db.Column(db.String(200))
    rol = db.Column(db.String(8), nullable=False, default='2')

    def __init__(self, nombre, apellido, nombre_usuario, correo, contrasena, sexo, pais=None, imagen=None, rol='2'):
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_usuario = nombre_usuario
        self.correo = correo
        self.contrasena = generate_password_hash(contrasena)
        self.sexo = sexo
        self.pais = pais
        self.imagen = imagen
        self.rol = rol

    def __repr__(self):
        return f"<Usuario {self.nombre_usuario}>"

# Crear tablas
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')

@app.route('/trailers')
def trailers():
    return render_template('trailers.html')

@app.route('/reseñas')
def reseñas():
    return render_template('reseñas.html')

@app.route('/actualizarPerfil')
def actualizarPerfil():
    return render_template('actualizarPerfil.html')

@app.route('/foro')
def foro():
    if session.get('logueado'):
        return render_template('foro.html')
    else:
        mensaje = 'Por favor inicia sesión para acceder al foro.'
        return render_template('iniciar-sesion.html', mensaje=mensaje)

@app.route('/tabla_usuarios')
def tabla_usuarios():
    usuarios = Usuario.query.all()
    return render_template('tabla_usuarios.html', usuarios=usuarios)

@app.route('/ingresar_usuario')
def ingresar_usuario():
    return render_template('ingresar_usuario.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/usuario', methods=['GET'])
def usuario():
    all_registros = Usuario.query.all()
    data_serializada = [{
        "id": u.id,
        "nombre": u.nombre,
        "apellido": u.apellido,
        "nombre_usuario": u.nombre_usuario,
        "correo": u.correo,
        "sexo": u.sexo,
        "pais": u.pais,
        "rol":u.rol,
        "imagen": u.imagen,
        
    } for u in all_registros]
    return jsonify(data_serializada)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        cambios = False
        campos = ['nombre', 'apellido', 'nombre_usuario', 'correo', 'sexo', 'pais', 'imagen', 'rol']
        
        for campo in campos:
            valor_nuevo = request.form.get(campo)
            if getattr(usuario, campo) != valor_nuevo:
                setattr(usuario, campo, valor_nuevo)
                cambios = True

        contrasena_nueva = request.form.get('contrasena')
        if contrasena_nueva and not check_password_hash(usuario.contrasena, contrasena_nueva):
            usuario.contrasena = generate_password_hash(contrasena_nueva)
            cambios = True

        if cambios:
            db.session.commit()
            return redirect(url_for('tabla_usuarios', mensaje='modificado'))
        else:
            return redirect(url_for('tabla_usuarios', mensaje='sin_cambios'))
    else:
        return render_template('editar_usuario.html', usuario=usuario)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or request.files['file'].filename == '':
        return redirect(request.url)
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return jsonify({"mensaje": "Archivo subido exitosamente", "ruta": path})

@app.route('/form', methods=['GET', 'POST'])
def registrarForm():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        nombre_usuario = request.form['nombreUsuario']
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        sexo = request.form['sexo']
        pais = request.form.get('pais')
        rol = request.form['rol']
        imagen = None

        if 'img-usuario' in request.files:
            file = request.files['img-usuario']
            if file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                imagen = path
        

        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            nombre_usuario=nombre_usuario,
            correo=correo,
            contrasena=contrasena,
            sexo=sexo,
            pais=pais,
            rol=rol,
            imagen=imagen,
           
        )

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('index', msg='Usuario registrado con éxito'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar usuario: {str(e)}")
            return redirect(url_for('index')), 500
    return render_template('registrarse.html', msg='Método HTTP incorrecto')

@app.route('/iniciar-sesion', methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == 'GET':
        return render_template('iniciar-sesion.html')

    correo = request.form['correo']
    contrasena = request.form['contrasena']
    usuario = Usuario.query.filter_by(correo=correo).first()

    if usuario and check_password_hash(usuario.contrasena, contrasena):
        session['logueado'] = True
        if usuario.rol == '2':
            return render_template("usuarioRegistrado.html")
        elif usuario.rol == '1':
            return redirect(url_for('tabla_usuarios'))
        else:
            return render_template("cerrar.html", mensaje="Rol de usuario no válido o indefinido")
    else:
        return render_template("cerrar.html", mensaje="Usuario o contraseña incorrectos")

@app.route('/cerrar-sesion')
def cerrar_sesion():
    session.clear()
    return redirect(url_for('index'))

@app.route('/borrar/<int:id>', methods=['DELETE'])
def borrar(id):
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return redirect(url_for('tabla_usuarios'))
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404
  

@app.route("/registro", methods=['POST']) 
def registro():
    try:
        data = request.get_json()
        campos = ['nombre', 'apellido', 'nombre_usuario', 'correo', 'contrasena', 'sexo', 'pais', 'imagen', 'rol']
        if not all(field in data for field in campos):
            return {"error": "Faltan campos obligatorios"}, 400

        nuevo_registro = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            nombre_usuario=data['nombre_usuario'],
            correo=data['correo'],
            contrasena=data['contrasena'],
            sexo=data['sexo'],
            pais=data['pais'],
            imagen=data['imagen'],
            rol=data['rol']
        )
        db.session.add(nuevo_registro)
        db.session.commit()

        return {"message": "Registro creado exitosamente", "usuario_id": nuevo_registro.id}, 201

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
