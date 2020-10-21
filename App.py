from flask import Flask,render_template,url_for

app = Flask(__name__)

@app.route('/')
def Landing():
    return render_template('Landing.html') 

@app.route('/Home')
def Home():
    return 'Home'
@app.route('/About')
def About():
    return 'About'
@app.route('/login')
def login():
    return render_template('Login.html')
if __name__ == '__main__':
    app.run(port = 3000, debug = True)
