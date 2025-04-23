import mysql.connector as sql
import random
from flask import Flask, render_template,request,url_for, redirect
conn = sql.connect(host = "localhost", user = "root" ,passwd = "HPSroot123*", database = "nie")
app = Flask(__name__)


def id_generator():
    c.execute("select id from user_access")
    row1 = c.fetchall()
    c.execute("select id from seller_access")
    row2 = c.fetchall()
    temp = []
    temp1 = []
    temp2 = []
    for i in row1:
        temp.append(i[0])
        temp1.append(i[0])
    for i in row2:
        temp.append(i[0])
        temp2.append(i[0])
    while True:
        new_id = random.randint(1000, 9999)
        if new_id not in temp:
            return new_id

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
    c.execute("Select pass from user_access where id = '{}'".format(uname))
    row1 = c.fetchone()
    c.execute("Select pass from seller_access where id = '{}'".format(uname))
    row2 = c.fetchone()
    if row1 != None:
        if (row1[0]==int(password)):
            return render_template('buyer_dashboard.html')
        else:
            return "Invalid Credentails"
    elif row2 != None:
        if(row2[0]==int(password)):
            return render_template('seller_dashboard.html')
        else:
            return "Invalid Credentails"
    else:
        return "Not registered under seller or Buyer"
    

@app.route('/Register', methods = ["POST","GET"])
def register():
    return render_template('register.html')

@app.route('/Register2',methods = ["POST", "GET"])
def register2():
    uname = request.form["name"]
    password = request.form["pass"]
    phone = request.form["phone"]
    access = request.form["access"]
    id = id_generator()
    c.execute("insert into {} values('{}','{}','{}','{}')".format(access, id, password, uname, phone))
    conn.commit()
    return redirect(url_for('login'))

@app.route('/sellProp', methods = ["POST","GET"])
def sellProp():
    return render_template("Sell_Property.html")

@app.route("/leaseProp", methods=["POST","GET"])
def leaseProp():
    return render_template("Lease_Property.html")
@app.route('/buyProp', methods = ["POST","GET"])
def buyProp():
    return render_template("Buy_Property.html")

@app.route("/buyLeaseProp", methods=["POST","GET"])
def buyLeaseProp():
    return render_template("Buy_Lease_Property.html")

@app.route('/createAcc',methods=['POST','GET'])
def createAcc():
    return render_template("createAccount.html")

@app.route('/sellDetails',methods=['POST','GET'])
def sellDetails():
    sid1 = request.form["sellerId"]
    city1 = request.form["city"]
    landMark1 = request.form["landmark"]
    loc1 = request.form["location"]
    rate1 = request.form["price"]
    if not sid1 or not city1 or not landMark1 or not loc1 or not rate1:
        return render_template("Sell_Property.html")
    # c.execute("insert into properties_on_sale values('{}','{}','{}','{}',Null)".format(city1,landMark1,loc1,rate1))
    c.execute("INSERT INTO properties_on_sale (city, landmark, location, quote_price) VALUES (%s, %s, %s, %s)", (city1, landMark1, loc1, rate1))
    pay_rate = (3/100)*float(rate1)
    conn.commit()
    return render_template("sellConfirmation.html",p_r=pay_rate)

@app.route('/buyDetails',methods=['GET','POST'])
def buyDetails():
    bid1 = request.form.get("buyId")
    b_city1 = request.form.get("buyCity")
    b_loc1 = request.form.get("buyLoc")
    if not bid1 or not b_city1:
        return render_template("Buy_Property.html")
    elif not b_loc1:
        c.execute("select * from properties_on_sale where city='{}' and b_id is NULL".format(b_city1))
    else:
        c.execute("select * from properties_on_sale where city='{}' and location='{}' and b_id is NULL".format(b_city1,b_loc1))
    ans = c.fetchall()
    return render_template("Buy_Property.html",data=ans,message="No sellers found for this location currently or maybe try just the city")
if __name__ == "__main__":
    app.run(debug = True)

