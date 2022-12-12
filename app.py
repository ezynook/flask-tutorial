from flask import *
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = 'MjkwOQ=='

#Database Connect
def dbConnect():
    try:
        engine = create_engine('sqlite:///flask.db')
        return engine
    except Exception as e:
        print('Error -> ', e)

#Index Page
@app.route("/")
def index():
    if session.get("username") == None:
        return render_template("index.html")
    else:
        return redirect(url_for('showdata'))

#Login
@app.route("/home", methods=["POST"])
def login():
    cur = dbConnect()
    username = request.form.get('username')
    password = request.form.get('password')
    statement = f"SELECT username, password from users WHERE username='{username}' AND password = '{password}';"
    rows = cur.execute(statement).fetchone()
    if not rows:
        return render_template("index.html", data="Login Failed")
    else:
        session['username'] = username
        return redirect(url_for('showdata'))

#Signup-page
@app.route("/signup-page")
def signup_page():
    return render_template('signup.html')

#Signup
@app.route("/signup", methods=['POST'])
def signup():
    conn = dbConnect()
    username = request.form['username']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    nickname = request.form['nickname']
    conn.execute(f"INSERT INTO users (username,password,fname,lname,nickname) VALUES ('{username}','{password}','{fname}','{lname}','{nickname}')")
    conn.commit()
    flash("Signup Successfully!")
    return render_template('index.html')

#Show Data
@app.route('/showdata')
def showdata():
    if session.get("username") == None:
        return redirect(url_for("index"))
    else:
        conn = dbConnect()
        sql = "SELECT * FROM main.users"
        df = pd.read_sql(sql , conn)
        mydict = df.to_dict('records')
        return render_template("showdata.html", data=mydict, session=session['username'])

#Add Page
@app.route('/add')
def add():
    return render_template('add.html')
#Add Data
@app.route('/adddata', methods=['POST'])
def adddata():
    conn = dbConnect()
    username = request.form['username']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    nickname = request.form['nickname']
    conn.execute(f"INSERT INTO users (username,password,fname,lname,nickname) VALUES ('{username}','{password}','{fname}','{lname}','{nickname}')")
    conn.commit()
    flash("Save Data Successfully!")
    return render_template('add.html')
#Edit page
@app.route('/edit/<id_data>')
def edit(id_data):
    conn = dbConnect()
    sql = f"SELECT * FROM users where id = {id_data}"
    df = pd.read_sql(sql , conn)
    mydict = df.to_dict('records')
    return render_template("edit.html", data=mydict)
#Edit Data
@app.route('/editdata', methods=['POST'])
def editdata():
    conn = dbConnect()
    fname = request.form['fname']
    lname = request.form['lname']
    nickname = request.form['nickname']
    id = request.form['id']
    sql = f"UPDATE users SET fname = '{fname}', lname = '{lname}', nickname = '{nickname}' WHERE id = {id}"
    conn.execute(sql)
    conn.commit()
    return redirect(url_for('showdata'))
#Delete
@app.route('/delete/<id_data>')
def delete(id_data):
    conn = dbConnect()
    conn.execute(f"DELETE from users where id = {id_data}")
    conn.commit()
    return redirect(url_for('showdata'))

#Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)