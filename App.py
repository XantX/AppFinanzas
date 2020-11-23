from flask import Flask,render_template,request,redirect, url_for,session, flash
from flask_mysqldb import MySQL
import bcrypt
from datetime import date
from datetime import datetime, timedelta

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
        return redirect(url_for('main'))
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
        # Busca los clientes
        QueryClientes = "SELECT CL.DNI,CL.name,CL.imgprofile,CU.Saldo FROM cliente CL, cuenta CU WHERE CU.storeid = %s and CU.idcliente = CL.id"
        cur.execute(QueryClientes,[session['email']])
        dato = cur.fetchall()
        ### tabla de divisas
        Query="SELECT * FROM divisa"
        cur.execute(Query)
        divisa = cur.fetchall()
        ## Tabla de periodos
        cur.execute("SELECT * FROM periododepago")
        Periodo = cur.fetchall()
        return render_template('monefay.html',divisas = divisa,Periodos = Periodo, datos = dato)
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
        ### Tabla de cuenta Busqueda de email
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
    querySearchCliente = "SELECT cu.idcliente FROM cliente cl, cuenta cu WHERE cl.dni = %s and cu.storeid = %s"
    cur.execute(querySearchCliente,[cuenta,session['email']])
    ident = cur.fetchone()
    print("El datos es:",ident)
    cur.execute('DELETE FROM cuenta WHERE idcliente = {0}'.format(ident[0]))
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
        ### Consumo de tabla cuenta
        query = "SELECT cl.dni FROM cliente cl, cuenta cu WHERE cl.dni = %s and cu.storeid = %s"
        cur.execute(query,[dni,session['email']])
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
        divisa = request.form['divisa']
        activacion = request.form['CostoActivacion']
        cierre = request.form['cierre']
        Periodo = request.form['Periodo']
        PeriodoMantenimiento = request.form['PeriodoMantenimiento']
        montoMantenimiento = request.form['montoMantenimiento']

        cur = mysql.connection.cursor()
        ### Ingreso de datos de direccion 
        QueryDirrecion = "INSERT INTO direccion (Lote, Manzana, Calle,Distrito,NumeroCasa) VALUES(%s,%s,%s,%s,%s)"
        cur.execute(QueryDirrecion,(lote,Manzana,calle,Distrito,numeroCasa))
        mysql.connection.commit()
        ### Interes
        QueryInteres = "INSERT INTO interes (Cperiodo,TipoInteres,Porcentaje) VALUES(%s,%s,%s)"
        cur.execute(QueryInteres,(Periodo,tipoTasa,tasa_porcentaje))
        mysql.connection.commit()
        ### Mantenimiento
        QueryMantenimiento = "INSERT INTO mantenimiento (Cperiodo,monto) VALUES(%s,%s)"
        cur.execute(QueryMantenimiento,(PeriodoMantenimiento,montoMantenimiento))
        mysql.connection.commit()
        ### Codes de Direecion
        DataDireccion = "SELECT MAX(cDireccion) FROM direccion"
        cur.execute(DataDireccion)
        Cdireccion = cur.fetchone()
        ### Code Interes
        DataDireccion = "SELECT MAX(cInteres) FROM Interes" 
        cur.execute(DataDireccion)
        CInteres = cur.fetchone()
        ### Code mantenimiento
        DataDireccion = "SELECT MAX(cMantenimiento) FROM mantenimiento"
        cur.execute(DataDireccion)
        CMantenimiento = cur.fetchone()
        ### Cliente
        QueryCliente = "INSERT INTO cliente (dni,direccion,name,lastnameF,lastnameM,phone,correo,imgprofile) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(QueryCliente,(dni,Cdireccion,name,lastnameF,lastnameM,phone,email,perfil))
        mysql.connection.commit()
        ### Code Cliente
        DataCliente = "SELECT MAX(id) FROM cliente"
        cur.execute(DataCliente)
        CCliente = cur.fetchone()
        ###Inset Cuenta
        QueryCuenta = "INSERT INTO cuenta (idcliente,storeid,Saldo,Cierre,CDivisa,Activacion,Cmantenimiento,Cinteres,limite) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(QueryCuenta,(CCliente,storeid,limite,cierre,divisa,activacion,CMantenimiento,CInteres,limite))
        mysql.connection.commit()


    return redirect(url_for('main'))

def deuda(movimientos,periodo,tasa):
    
    def formula(retiro,tasa,FechaRetiro,DiasPeriodo):
        # print(round((today2-FechaRetiro).days/DiasPeriodo,3))
        difDays = round((today2-FechaRetiro).days/DiasPeriodo,3)
        valB = float(1 + tasa/100)
        val = valB** (difDays)
        return  retiro*val 
    today2 = datetime.now() ## Dia actual
    new_date = datetime(2020,10,15,0,0,00,0000)
    deudaTotal = 0
    for i in movimientos:
        if i[6] == 1:
            if periodo == "Mensual":
                deudaTotal += formula(i[4],tasa,i[5],30)
            if periodo == "Semanal":
                deudaTotal += formula(i[4],tasa,i[5],7)
    print(deudaTotal)
    return deudaTotal

def SaldoActual():
    pass
### Perfil de cuenta
@app.route("/monefay/<string:cuenta>") 
def cuenta(cuenta):
    cur = mysql.connection.cursor()
    ### Tabla de movimientos
    QueryMovimientos = "SELECT * FROM movimiento WHERE Cliente = %s and Usuario = %s"
    cur.execute(QueryMovimientos,[cuenta,session['email']])
    movimiento = cur.fetchall()
    ### tabla de divisas
    Query="SELECT * FROM divisa"
    cur.execute(Query)
    divisa = cur.fetchall()
    ## Tabla de periodos
    cur.execute("SELECT * FROM periododepago")
    Periodo = cur.fetchall()
    ## Obtiene los datos de una cuenta
    queryCliente = "SELECT CL.name,CL.lastnameF,CL.lastnameM,CL.imgprofile,CL.phone,CU.Saldo,inte.TipoInteres,PER.Periodo,DIVI.TipoDivisa,CU.Contratado,CU.id,CU.limite,CL.dni,inte.porcentaje FROM cuenta CU JOIN cliente CL ON CU.idcliente = CL.id JOIN interes inte ON CU.Cinteres = inte.CInteres JOIN mantenimiento man ON CU.Cmantenimiento = man.CMantenimiento JOIN periododepago PER ON inte.CPeriodo = PER.CPeriodo JOIN divisa DIVI ON CU.CDivisa = DIVI.CDivisa WHERE CL.dni = %s"
    cur.execute(queryCliente,[cuenta])
    datosCuenta = cur.fetchall()
    ### Calculando la deuda
    deudaTotal = deuda(movimiento,datosCuenta[0][7],datosCuenta[0][13])
    return render_template('monefaycuenta.html',datoscuenta = datosCuenta,divisas = divisa,Periodos = Periodo,movimientos = movimiento,deuda = deudaTotal)

### Funcion de retiro
@app.route("/retiro", methods=['POST','GET'])
def retiro():
    if request.method == 'POST':
        dni = request.form['dni']
        id = request.form['id']
        texto = request.form['DescripcionDeRetiro']
        monto = request.form['MontoRetiro']

        cur = mysql.connection.cursor()
        ### Se agrega un movimiento
        QueryMovimiento = "INSERT INTO movimiento (idcliente,Cliente,Usuario,Monto,TipoDeMovimiento,descripcion) VALUES(%s,%s,%s,%s,%s,%s)"
        cur.execute(QueryMovimiento,(id,dni,session['email'],monto,1,texto))
        mysql.connection.commit()
        ### Se hace el calculo de el saldo
        QueryUpdate = "UPDATE cuenta SET Saldo = Saldo - %s WHERE id = %s"
        cur.execute(QueryUpdate,[monto,id])
        mysql.connection.commit()
        direccion = "/monefay/" + dni
    return redirect(direccion) 

### Funcion Cobro    
@app.route("/cobro",methods=['POST','GET'])
def Cobro():
    if request.method == 'POST':
        dni = request.form['dni']
        id = request.form['id']
        texto = request.form['DescripcionDeCobro']
        monto = request.form['MontoCobro']

        cur = mysql.connection.cursor()
        ### Insertar movimiento
        QueryMovimiento = "INSERT INTO movimiento (idcliente,Cliente,Usuario,Monto,TipoDeMovimiento,descripcion) VALUES(%s,%s,%s,%s,%s,%s)"
        cur.execute(QueryMovimiento,(id,dni,session['email'],monto,0,texto))
        mysql.connection.commit()

        ### Se hace el calculo de el saldo
        QueryUpdate = "UPDATE cuenta SET Saldo = Saldo + %s WHERE id = %s"
        cur.execute(QueryUpdate,[monto,id])
        mysql.connection.commit()
        direccion = "/monefay/" + dni
        ### Deuda

    return redirect(direccion) 
### Funcion para salir
@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for('Landing'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
