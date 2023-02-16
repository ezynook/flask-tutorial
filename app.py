from flask import *
import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'MjkwOQ=='
BASEPATH = os.path.abspath(os.getcwd())
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASEPATH}/flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
   __tablename__ = 'users'
   id = db.Column(db.Integer, primary_key = True)
   username = db.Column(db.String(50))
   password = db.Column(db.String(20))  
   fname = db.Column(db.String(20))  
   lname = db.Column(db.String(20))  
   nickname = db.Column(db.String(20))

def __init__(self, id, username, password,fname, lname, nickname):
   self.id = id
   self.username = username
   self.password = password
   self.fname = fname
   self.lname = lname
   self.nickname = nickname

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
    c_username = request.form.get('username')
    c_password = request.form.get('password')
    check = users.query.filter_by(username = c_username, password = c_password).all()
    if not check:
        flash('Login Failure')
    else:
        session['username'] = c_username
        return redirect(url_for('showdata', page_num=1, filter = None))

#Signup-page
@app.route("/signup-page")
def signup_page():
    return render_template('signup.html')

#Report
@app.route("/report")
def report():
    today = datetime.now()
    dt = today.strftime('%d/%m/%Y %H:%M:%S')
    result = users.query.all()
    return render_template('report.html', data=[result,dt])

#Signup
@app.route("/signup", methods=['POST'])
def signup():
    user = users(
        username = request.form['username'],
        password = request.form['password'],
        fname = request.form['fname'],
        lname = request.form['lname'],
        nickname = request.form['nickname']
    )
    db.session.add(user)
    db.session.commit()
    flash("Signup Successfully!")
    return render_template('index.html')

#Show Data
@app.route('/showdata/<int:page_num>', methods=['GET'])
def showdata(page_num):
    filter = request.args.get('filter')
    if session.get("username") == None:
        return redirect(url_for("index"))
    else:
        if filter:
            result = users.query.filter(users.fname.like('%%'+filter+'%%')).paginate(per_page=3, page=page_num, error_out=False)
        else:
            result = users.query.paginate(per_page=3, page=page_num, error_out=False)
        
        return render_template("showdata.html", data=result, session=session['username'], pagelength=page_num)

#Add Page
@app.route('/add')
def add():
    return render_template('add.html')
#Add Data
@app.route('/adddata', methods=['POST'])
def adddata():
    user = users(
        username = request.form['username'],
        password = request.form['password'],
        fname = request.form['fname'],
        lname = request.form['lname'],
        nickname = request.form['nickname']
    )
    db.session.add(user)
    db.session.commit()
    flash("Save Data Successfully!")
    return render_template('add.html')
#Edit page
@app.route('/edit/<id_data>')
def edit(id_data):
    sql = users.query.filter_by(id = id_data).all()
    return render_template("edit.html", data=sql)
#Edit Data
@app.route('/editdata', methods=['POST'])
def editdata():
    item = users.query.get(request.form['id'])
    item.fname = request.form['fname']
    item.lname = request.form['lname']
    item.nickname = request.form['nickname']
    db.session.commit()
    return redirect(url_for('showdata', page_num=1, filter = None))
#Delete
@app.route('/delete/<id_data>')
def delete(id_data):
    users.query.filter_by(id=id_data).delete()
    db.session.commit()
    return redirect(url_for('showdata', page_num=1, filter = None))

#Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)