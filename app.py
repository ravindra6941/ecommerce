from flask import Flask,render_template,session,request, redirect, url_for
from library import*
from flask_session import Session
from datetime import datetime
import random

app = Flask(__name__)
ob=library()
import app2
import login
app.secret_key = 'kjfhdskjfh sfkjshd'


@app.route('/')
def home():
	data=ob.getdata("product","popular","1")
	session['cate_menu']=ob.getdata("category")
	return render_template('frontend/home.html',err=data)

@app.route('/contact')
def contact():
   return render_template('frontend/contact.html')

@app.route('/blog')
def blog():
   return render_template('frontend/blog.html')

@app.route("/showorder")
def showorders():
   err=""
   qry="select A.Order_id, A.Customer_id, A.o_date,B.product_name, B.price, B.image, A.shipped, A.confirm  from myorder A  join product B  on A.product_id = B.product_id"
   data=ob.getQryData(qry)
   return render_template("dash/showorder.html",err=data['data'])

@app.route("/shippedOrder/<id>")
def shippedOrder(id):
    Qry="select * from myorder A join shipping B on A.order_id=B.order_id and A.order_id="+id
    data=ob.getQryData(Qry)
    #return render_template("dash/ShippingDone.html",err=[data])
    return redirect("/showorder")

@app.route("/OrderCompleted/<id>")
def OrderCompleted(id):
    ob.update("myorder",{"confirm":1},"order_id",id)
    ob.update("shipping",{"delivered":datetime.now()},"order_id",id)
    return redirect("/showorder")

@app.route("/shipping", methods=['GET','POST'])
def shipping():
    err=""
    if(request.method=="POST" and 'cart' in session):
        name=request.form["xuser"]
        email=request.form["xemail"]
        mobile=request.form["xmobile"]
        address=request.form["xadd"]
        city=request.form["xcity"]
        zipcode=request.form["xcode"]
        oid=random.randint(111111111,99999999999)
        x=0
        for row in session['cart']:
            data={"order_id":oid,"customer_id":session['userid'] ,"product_id":session['cart'][x][1],"O_date":datetime.now(),"cancel":0}
            data=ob.insert("myorder",data)
            x=x+1
        if(data['status']==True):
            x=0
        for row in session['cart']:
            data={"product_id":session['cart'][x][0],"order_id":oid,"Customer_id":session['userid'],"address":address,"city":city,"zipcode":zipcode,"ship_date":"0000-00-00","delivered":"0000-00-00"}
            ob.insert("shipping",data)
            x=x+1
        session.pop('cart',"None")
        session.pop('count',"None")
        session.pop('cart',"None")
    return render_template("frontend/billing.html")


@app.route("/shippingDone",methods=['GET','POST'])
def shippingDoneCompleted():
    if(request.method=="POST"):
        orderid=request.form['OrderId']
        shipid=request.form['ShipId']
        ob.update("myorder",{"shipped":1},"order_id",orderid)
        ob.update("shipping",{"ship_date":datetime.now()},"ship_id",shipid)
        return redirect(url_for("showorder"))
    else:
        return redirect(url_for("showorder"))

@app.route("/delCustomer/<id>/<x>")
def del_product(id,x):
    if(x=="1"):
        data={"active":0}
    else:
        data={"active":1}

    ob.update("product",data,"id",id)
    return redirect(url_for("showorder"))

if __name__ == '__main__':
   app.run(debug=True)

