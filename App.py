from flask import Flask,render_template,request,redirect, url_for,session, flash
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
    if 'email' in session:
        return render_template('monefay.html')
    else:
        return render_template('Landing.html') 

@app.route('/login')
def login():
    if 'email' in session:
        return render_template('monefay.html')
    else:
        return render_template('Login.html')
@app.route('/monefay')
def main():
    if 'email' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT DNI, name, perfilimg FROM cuenta WHERE storeid = %s', [session['email']])
        data = cur.fetchall()
        return render_template('monefay.html', datos = data)
    else:
        return render_template('Landing.html')

@app.route('/registro')
def registro():
    if 'email' in session:
        return render_template('monefay.html')
    else:
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
            flash("Llene todos los campos", "alert-warning")
            return redirect(url_for('registro'))

        cur = mysql.connection.cursor()
        sQuery = "SELECT email FROM usuario WHERE email = %s"
        cur.execute(sQuery,[email])
        usuario = cur.fetchone()
        cur.close()
        if usuario != None:
            flash("El correo ingresado ya esta registrado", "alert-warning")
            return redirect(url_for('registro'))

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO usuario (email,user,lastnameF,lastnameM,RUC,password,store,DNI) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)',
                (email,name,lastnameF,lastnameM,RUC,contrasena_encrypt,store,DNI))
        mysql.connection.commit()
        session['email'] = email
    return redirect(url_for('login')) 

### Datos de el formulatio de landing para registro
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
### Funciones de login 
@app.route('/loginIn',methods=['POST','GET'])
def loginin():
    if request.method == 'GET':
        if 'email' in session:
            return render_template('monefay.html')
        else:
            return render_template('login')
    else:
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            flash("Llene todos los campos", "alert-warning")
            return redirect(url_for('login'))
        password_encode = password.encode("utf-8")
        cur = mysql.connection.cursor()
        sQuery = "SELECT email, password FROM usuario WHERE email = %s"
        cur.execute(sQuery,[email])
        usuario = cur.fetchone()
        cur.close()
        if (usuario != None):
            password_encriptado_encode = usuario[1].encode()
            if (bcrypt.checkpw(password_encode,password_encriptado_encode)):
                session['email'] = usuario[0] 
                return redirect(url_for('main'))
            else:
                flash("El password no se correcto", "alert-warning")
                return redirect(url_for('login')) 

        else:
            flash("El correo no existe", "alert-warning")
            return redirect(url_for('login'))

            
    return redirect(url_for('main'))
@app.route("/delete/<string:cuenta>")
def delete(cuenta):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM cuenta WHERE DNI = {0}'.format(cuenta))
    mysql.connection.commit()
    return redirect(url_for('main'))
### Registrar cuenta 
@app.route("/cuentaRes",methods=['POST','GET'])
def cuentaRes():
    if request.method == 'POST':
        ## Captura de datos 
        ### datos personales
        ## Verificar dni
        dni = request.form['dni']
        cur = mysql.connection.cursor()
        query = "SELECT DNI FROM cuenta WHERE DNI = %s"
        cur.execute(query,[dni])
        cuenta = cur.fetchone()
        cur.close()
        if(cuenta != None):
            print("ya existe el dni")
            flash("El dni ya existe", "alert-warning")
            return redirect(url_for('main'))
        storeid = session['email']
        perfil = request.form['perfil']
        name = request.form['name']
        lastnameF = request.form['lastnameF']
        lastnameM = request.form['lastnameM']
        phone = request.form['phone']
        email = request.form['email']
        ## Datos de direccion
        Departamento = request.form['Departamento']
        Distrito = request.form['Distrito']
        lote = request.form['lote']
        Manzana = request.form['Manzana']
        calle = request.form['calle']
        numeroCasa = request.form['NumerodeCasa']
        ### Datos de linea
        tipoTasa = request.form['tipoTasa']
        tasa_porcentaje = request.form['porcentTasa']
        limite = request.form['limite']
        mantenimiento = request.form['Mantenimiento']
        divisa = request.form['divisa']
        activacion = request.form['CostoActivacion']
        ### Ingreso de datos personales
        cur = mysql.connection.cursor()
        Query = "INSERT INTO cuenta (DNI,storeid,name,perfilimg,lastnameF,lastnameM,telefono,email,Departamento,Distrito,Lote,Manzana,Calle,Numero) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        cur.execute(Query,(dni,storeid,name,perfil,lastnameF,lastnameM,phone,email,Departamento,Distrito,lote,Manzana,calle,numeroCasa))
        mysql.connection.commit()
        ### Ingreso de datos de credito
        sQuery = "INSERT INTO credito (idlinea,tipodetasa,porcentaje,limite,mantenimiento,divisa,activacion) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sQuery,(dni,tipoTasa,tasa_porcentaje,limite,mantenimiento,divisa,activacion))
        mysql.connection.commit()
    return redirect(url_for('main'))

@app.route("/monefay/<string:cuenta>") 
def cuenta(cuenta):
    return render_template('monefaycuenta.html')
### Funcion para salir
@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for('Landing'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
