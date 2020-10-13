from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def Landing():
    return render_template('Landing Page/Landing.html') 

@app.route('/Home')
def Home():
    return 'Home'
if __name__ == '__main__':
    app.run(port = 3000, debug = True)
