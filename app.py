from flask import *
import pandas as pd
import sqlite3 as sql
from Route.ShowData import showdata

app = Flask(__name__)
app.secret_key = 'MjkwOQ=='
app.register_blueprint(showdata)

def dbConnect():
    try:
        con = sql.connect("flask.db")
        cur = con.cursor()
        return [con, cur]
    except Exception as e:
        print('Error -> ', e)

@app.route("/")
def index():
    if session.get("username") == None:
        return render_template("index.html")
    else:
        return render_template("home.html", data=session['username'])
    
    
@app.route("/home", methods=["POST"])
def login():
    cur = dbConnect()[1]
    username = request.form.get('username')
    password = request.form.get('password')
    statement = f"SELECT username, password from users WHERE username='{username}' AND password = '{password}';"
    cur.execute(statement)
    if not cur.fetchone():
        return render_template("index.html", data="Login Failed")
    else:
        session['username'] = username
        return render_template("home.html", data=username)
@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)