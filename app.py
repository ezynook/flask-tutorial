from flask import *
import pandas as pd
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'MjkwOQ=='

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

@app.route('/showdata')
def showdata():
    if session.get("username") == None:
        return redirect(url_for("index"))
    else:
        conn = dbConnect()[0]
        sql = "SELECT * FROM main.users"
        df = pd.read_sql(sql , conn)
        mydict = df.to_dict('records')
        return render_template("showdata.html", data=mydict)

@app.route('/edit/<id_data>')
def edit(id_data):
    conn = dbConnect()[0]
    sql = f"SELECT * FROM users where id = {id_data}"
    df = pd.read_sql(sql , conn)
    mydict = df.to_dict('records')
    return render_template("edit.html", data=mydict)

@app.route('/editdata', methods=['POST'])
def editdata():
    conn = dbConnect()[0]
    fname = request.form['fname']
    lname = request.form['lname']
    nickname = request.form['nickname']
    id = request.form['id']
    sql = f"UPDATE users SET fname = '{fname}', lname = '{lname}', nickname = '{nickname}' WHERE id = {id}"
    conn.execute(sql)
    conn.commit()
    return redirect(url_for('showdata'))

@app.route('/delete/<id_data>')
def delete(id_data):
    conn = dbConnect()[0]
    conn.execute(f"DELETE from users where id = {id_data}")
    conn.commit()
    return redirect(url_for('showdata'))

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/adddata', methods=['POST'])
def adddata():
    conn = dbConnect()[0]
    username = request.form['username']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    nickname = request.form['nickname']
    conn.execute(f"INSERT INTO users (username,password,fname,lname,nickname) VALUES ('{username}','{password}','{fname}','{lname}','{nickname}')")
    conn.commit()
    flash("Save Data Successfully!")
    return render_template('add.html')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)