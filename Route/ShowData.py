from flask import *
import sqlite3
import pandas as pd

showdata = Blueprint('showdata', __name__)

def dbConnect():
    try:
        con = sqlite3.connect("flask.db")
        cur = con.cursor()
        return [con, cur]
    except Exception as e:
        print('Error -> ', e)

@showdata.route('/showdata')
def adddata():
    if session.get("username") == None:
        return redirect(url_for("index"))
    else:
        conn = dbConnect()[0]
        sql = "SELECT * FROM main.users"
        df = pd.read_sql(sql , conn)
        mydict = df.to_dict('records')
        return render_template("showdata.html", data=mydict)
