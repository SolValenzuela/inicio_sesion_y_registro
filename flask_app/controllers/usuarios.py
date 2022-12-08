from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.usuario import Usuario

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 


#ruta de inicio
@app.route('/')
def ruta_inicio():
    return render_template('/index.html')


#ruta Post de formulario de registro de usuario,guarda los datos del nuevo usuario y redirige
@app.route('/registro/usuario', methods=['POST'])
def registro_usuario():
    is_valid= Usuario.validar_usuario(request.form)
    print(is_valid)
    if not is_valid:
        print('No valido')
        return redirect('/')
    
    nuevo_usuario ={
        "nombre":request.form['nombre'],
        "apellido":request.form['apellido'],
        "email": request.form['email'],
        "password":bcrypt.generate_password_hash(request.form['password'])
    }
    id = Usuario.save(nuevo_usuario)
    if not id:
        flash("Email ya existe.","register")
        return redirect('/')
    session['username'] = request.form['nombre']
    session['usuario_id'] = id
    return redirect('/dashboard')



#ruta Post de formulario login,comprueba que usuario existe,guarda datos de session y redirige
@app.route("/login",methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    usuario = Usuario.get_by_email(data)
    if not usuario:
        flash("Emai o password inválido","login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(usuario.password,request.form['password']):
        flash("Emai o password inválido","login")
        return redirect("/")
    session['usuario_id'] =usuario.id
    
    return redirect('/dashboard')


#Ruta que muestra el dashboard
@app.route('/dashboard')
def welcome():
    usuario=session['usuario_id']
    usuarios=Usuario.get_by_id(session['usuario_id'])
    return render_template('welcome.html',usuario=usuario,usuarios=usuarios)



#Ruta para desloguearse
@app.route('/logout')
def cerrar_sesion():
    session.clear()
    return redirect('/')




