import mysql.connector as sql
from flask import Flask, render_template,request,url_for
conn = sql.connect(host = "localhost", user = "root" ,passwd = "HPSroot123*", database = "NIE")
app = Flask(__name__)

c = conn.cursor()

if conn.is_connected():
    print("Connected")
else:
    print("Invalid")

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/dashboard', methods = ["POST","GET"])
def dashboard():
    uname = request.form["id"]
    password = request.form["pass"]
    if not uname or not password:
        return "INCOMPLETE CREDENTIALS"
    c.execute("Select pass from access where name = %s",(uname,))
    row = c.fetchone()
    if (row[0]==int(password)):
        return render_template('dashboard.html')
    else:
        return "Invalid Credentails"
    

@app.route('/sellProp', methods = ["POST","GET"])
def sellProp():
    return render_template("Sell_Property.html")

@app.route("/leaseProp", methods=["POST","GET"])
def leaseProp():
    return render_template("Lease_Property.html")

@app.route('/createAcc',methods=['POST','GET'])
def createAcc():
    return render_template("createAccount.html")
if __name__ == "__main__":
    app.run(debug = True)

