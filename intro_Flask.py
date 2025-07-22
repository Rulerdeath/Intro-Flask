#Primeramente, activamos el entorno virtual con ". .env/bin/activate."
#Con pip list puedes ver si Flask esta instalado junto con sus dependencias.
# si en algun momento quieres desactivar el entorno virtual, just type "deactivate"
#Siempre que queramos ejecutar la aplicacion, hay que activar el entorno virtual. Sino no sirve



from flask import Flask, render_template, url_for, request #Importamos el modulo flask y la clase Flask. Con url_for podemos crear rutas llamando las vistas
#render_template es una funcion que nos ayuda a poder renderizar plantillas HTML ubicadas en /template.
from datetime import datetime


app = Flask(__name__) #Representa nuestra aplicacion de Flask. Con esto le indicamos a Flask que este modulo (Email_snatcher) es el modulo prinicapl de la aplicacion
app.config.from_mapping(
    SECRET_KEY = 'dev'
)




# Crear Filtro personalizado
#@app.add_template_filter        #Decorador para poder definir y crear un filtro
def today(date):  #Esto es solo una funcion, pero lo que haremos sera agregarla a los filtros de Jinja para poder mostrar la fecha en formato DD/MM/YYYY. Se puede ver el uso del filtro en render.html. Se puede hacer usando el decorador @app.add_template_filter y definiendo la funcion debajo.
    return date.strftime('%d-%m-%Y')

app.add_template_filter(today, 'today') #O tambien podemos registrar el filtro de esta forma. Toma como argumentos el nombre de la funcion (today) y el nombre que le pondremos al filtro (today)

#funcion personalizada
@app.add_template_global
def repeat(s, n):  #Recibe un string y lo multiplica por el entero 'n'
    return s * n

#app.add_template_global(repeat, 'repeat')  #Tambien podemos pasar funciones de esta manera, para no tener que poner el nombre de la funcion en cada ruta cada vez que queramos pasarlo a una plantilla html



@app.route('/')  #Creamos nuestra ruta. Si lo colocamos con / indica que es la ruta princpal. Tambien podriamos cambiar la ruta de tal forma que el URL se vea asi: http://127.0.0.1:5000/hello si usamos @app.route('/hello')
def index(): #Representa la vista de nuestra aplicacion. Regresa un texto que dice "Hola mundo". Con esto ya podriamos ejecutar la app
    print(url_for("index")) #Imprime en la Terminal la ruta que te lleva a index  (/)
    print(url_for("hello"))
    print(url_for("code", code = 'print("Hola, esto es la funcion code!")'))
    return render_template("index.html")

#Para poder ejecutar y levantar la app, usamos "flask --app Email_Snatcher.py run". Esto lo corre localmente en http://127.0.0.1:5000 by default
#Para el modo debug, se debe correr con "-- debug" antes de "run". De esta manera, la app ya queda levantada y no hace falta detener todo para actualizar el codigo.

@app.route('/hello')  #Tambien podemos crear nuevas rutas, y para acceder a ellas cambiariamos el URL a lo que indique la ruta
def hello(): 
    return "<h1>Hola mundo</h1>" #Tambien podemos agregar etiquetas HTML

@app.route("/name")  # Varias rutas pueden dar a la misma vista. Si en el url aparece /name, /name/<name> o /name/<name>/<int:age> todas daran a la misma vista de la funcion "greeting"
@app.route("/name/<name>")
@app.route("/name/<name>/<int:age>") #Para anadir variables a rutas, se hace con <> y el nombre de la variable en medio. Tambien se puede especificar el tipo de valor a recibir (string, int, float, path, uuid)
def greeting(name = None, age = None): #Para poder dar uso a la variable, se pasa el argumento a la funcion. De esta manera adquirira el valor de cualquier cosa que escribamos en el URL en vez de <name>
    if name == None and age == None:  #Los if de abajo van a retornar un resultado distinto dependiendo de lo que el usuario indique en el URL.
        return "Hello world!"
    elif age == None:
        return f"<h2>This is my name: {name}! But I have no age!</h2>"
    else:
        return f"<h2>This is my name: {name}! And I am {age} years old! The double of that would be {age * 2}!</h2>"



from markupsafe import escape  # Sirve para hacer escapes HTML, osea que la vista pueda imprimir caracteres especiales en plaintext que otherwise serian interpreted como codigo.

@app.route("/code/<path:code>")
def code(code):
    return f"<code>{escape(code)}</code>"


#Filtro personalizado de la fecha de hoy
# from datetime import datetime. Eso esta al comienzo para mantener orden.

@app.route("/render")  #Esta funcion funciona en conjunto con render.html
def render_html():
    name = 'Alex'
    friends = ["Alan", "Melany", "Anderson", "Vale"]
    date = datetime.now()
    return render_template(
        "render.html",
        name = name,
        friends = friends,
        date = date
    ) #Usando esta funcion, pasamos la variable "name" como argumento de render_template para que pueda ser usada en render.html


@app.route("/hola")  # Varias rutas pueden dar a la misma vista. Si en el url aparece /name, /name/<name> o /name/<name>/<int:age> todas daran a la misma vista de la funcion "greeting"
@app.route("/hola/<name>")
@app.route("/hola/<name>/<int:age>")
@app.route("/hola/<name>/<int:age>/<email>") 
def saludo(name = None, age = None, email = None): #Para poder dar uso a la variable, se pasa el argumento a la funcion. De esta manera adquirira el valor de cualquier cosa que escribamos en el URL en vez de <name>
    my_data = {  #Creamos un diccionario para poder pasarlo a plantilla saludo.html
        'name' : name,
        'age' : age,
        'email' : email
    }
    return render_template('saludo.html', data = my_data)  #Regresamos el nombre de la plantilla en la que se usan los datos y el nombre que le daremos a la variable (data)



#Crear formulario wtform
from flask_wtf import FlaskForm  #Bibliioteca de Flask para poder hacer formularios mas facilmente en vez de usar HTML
from wtforms import StringField, PasswordField, SubmitField #Importa estas clases para el tipo string, password y submit
from wtforms.validators import DataRequired, Length #Imports the validators. Full list: https://wtforms.readthedocs.io/en/2.3.x/validators/

class RegisterForm(FlaskForm):
    username = StringField("Nombre de usuario: ", validators= [DataRequired(), Length(min=4, max= 25)])
    password = PasswordField("Password: ", validators= [DataRequired(), Length(min=6, max= 40)])  #Validators para poder validar la informacion del field de la contraseña.
    submit = SubmitField("Registrar: ")

#Registro de usuario
@app.route("/auth/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        return f"Nombre de usuario: {username}\nContraseña: {password}"
    # print(request.form)
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     if len(username) >= 4 and len(username) <= 25 and len(password) >= 6 and len(password) <= 40:
    #         return f"Nombre de usuario: {username}\nContraseña: {password}"
    #     else:
    #         error = """Nombre de usuario debe tener entre 4 y 25 caracteres y
    #         la contraseña debe tener entre 6 y 40 caracteres.
    #         """
    #         return render_template('auth/register.html', form = form, error = error)
    return render_template('auth/register.html', form = form)
