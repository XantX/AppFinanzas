from flask import Flask,render_template,request,redirect, url_for,session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'appfinanzas'

mysql = MySQL(app)

app.secret_key = "appLogin"

semilla = bcrypt.gensalt()

### Pagina de presentacion de la app 

@app.route('/')
def Landing():
    return render_template('Landing.html') 

@app.route('/login')
def login():
    return render_template('Login.html')
@app.route('/monefay')
def main():
    return render_template('monefay.html') 
@app.route('/registro')
def registro():
    return render_template('registro.html')

### Funciones de formularios 
@app.route('/registrar', methods=['POST','GET'])
def registrar():
    if request.method == 'POST':
        name = request.form['username']
        lastnameF = request.form['lastnameF']
        lastnameM = request.form['lastnameM']
        DNI = request.form['DNI']
        #encriptacion de contrasena
        contrasena = request.form['password']
        contrasena_encode = contrasena.encode("utf-8")
        contrasena_encrypt = bcrypt.hashpw(contrasena_encode,semilla)
        store = request.form['store']
        email = request.form['email']
        RUC = request.form['RUC']
        if not name or not lastnameF or not lastnameM or not DNI or not contrasena or not store or not email or not RUC:
            return redirect(url_for('registro'))
        print(contrasena_encode)

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuario (email,user,lastnameF,lastnameM,RUC,password,store,DNI) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                (email,name,lastnameF,lastnameM,RUC,contrasena_encrypt,store,DNI))
        mysql.connection.commit()
    return redirect(url_for('login')) 

@app.route('/seguridad', methods=['POST','GET'])
def seguridad():
    if request.method == 'POST':
        name = request.form['name']
        lastnameF = request.form['lastnameF']
        lastnameM = request.form['lastnameM']
        store = request.form['store']
        email = request.form['email']
    return render_template('registro.html',
            user=name,
            lastnameF=lastnameF,
            lastnameM = lastnameM,
            store = store,
            email = email) 

@app.route('/login',methods=['POST','GET'])
def loginin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            return redirect(url_for('login'))
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(port = 3000, debug = True)
