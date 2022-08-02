from flask import Flask,render_template,request,make_response,redirect,url_for,session
from flask_session import Session
from library import *
from __main__ import app
import requests
from cartlib import *
from werkzeug.utils import secure_filename
import random
import datetime

ob=library()
cart_ob=Cart()

@app.route("/admin")
def admin():
    return render_template('admin/login.html')

@app.route("/log", methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        email=request.form['email']
        password=request.form['password']
        if(email=="admin@gmail.com" and password=="admin"):
            return render_template("dash/index.html")
        else:
            return render_template("admin/login.html")

@app.route("/index")
def index():
   return render_template('index.html')

@app.route("/category")
def category():
   return render_template('dash/category.html')

@app.route("/cat", methods=['GET','POST'])
def cat():
    ret={}
    if request.method=="POST":
        catname=request.form['xcname']
        catdisc=request.form['xcdisc']
        upload=request.files['xfile']
        if(upload.save("static/upload/" + secure_filename(upload.filename))):
            ret={"mess":"File is not uploaded Plz Try Again","status":False}
        else:
            data={"image":upload.filename,"cat_name":catname,"cat_discription":catdisc}
            ret=ob.insert("category",data)
            ret={"mess":"Successfully insert data in Database","status":True}
    return render_template('/dash/category.html',err=ret)

@app.route("/logout")
def logout():
    return render_template("admin/login.html")

@app.route("/product")
def product():
    data=ob.getdata("category")
    return render_template('dash/product.html',err=data)

@app.route("/pro", methods=['GET','POST'])
def pro():
    if request.method=="POST":
        proname=request.form['xpname']
        prodisc=request.form['xpdisc']
        price=request.form['xprice']
        qnty=request.form['xqnty']
        file=request.files['xfile']
        cat_id=request.form['xcat']
        if(len(file.filename)>=2):
            file.save("static/upload/" + secure_filename(file.filename))
            data={"cat_id": cat_id,"image":file.filename, "product_name":proname,"pro_disc":prodisc,"price":price,"quantity":qnty}
        else:
            data={"cat_id":cat_id,"image":file.filename, "product_name":proname,"pro_disc":prodisc,"price":price,"quantity":qnty}

        ret=ob.insert("product",data)
        return redirect (url_for("product"))

    else:
        return render_template("/dash/product.html")

@app.route("/deldata/<id>")
def deldata(id):
    ob.deldata("product","product_id",id)
    return redirect(url_for('productdisp'))

@app.route("/edit/<id>")
def editdata(id):
    ret=ob.getdata("product","product_id",id)
    return render_template('/dash/edit.html',err=ret)

@app.route("/updatepro",methods=['GET','POST'])
def updatepro():
    if(request.method=="POST"):
        id=request.form['xid']
        proname=request.form['xpname']
        prodisc=request.form['xpdisc']
        price=request.form['xprice']
        qnty=request.form['xqnty']
        file=request.files['xfile']
        if(len(file.filename)>=2):
            file.save("static/upload/" + secure_filename(file.filename))
            data={"image":file.filename, "product_name":proname,"pro_disc":prodisc,"price":price,"quantity":qnty}
        else:
            data={"product_name":proname,"pro_disc":prodisc,"price":price,"quantity":qnty}
        ob.update("product",data,"product_id",id)
        return redirect(url_for('productdisp'))

@app.route("/productdisp")
def productdisp():
    data=ob.getdata("product")
    return render_template('/dash/productdisp.html',err=data)

@app.route("/billing", methods=['GET','POST'])
def billing():
    if request.method=="POST":
        name=request.form['xname']
        billadd=request.form['xbill']
        crnum=request.form['xcnum']
        crcvv=request.form['xcvv']
        crexpiry=request.form['xcexp']
        billdate=request.form['xcdate']
        data={"name":name,"billing_address":billadd,"creditcard_num":crnum,"creditcard_cvv":crcvv,"creditcard_expiry":crexpiry,"bill_date":billdate}
        data=ob.insert("billing",data)
    return render_template("frontend/payment.html")  

@app.route("/customer")
def customer():
    data=ob.getdata("customer")
    return render_template("dash/customer.html", err=data) 


@app.route("/order")
def order():
    return render_template("dash/order.html")  

@app.route("/subproduct/<id>")
def subproduct(id):
    data=ob.getdata("product","product_id",id)
    return render_template("frontend/subproduct.html",err=data)

@app.route("/CartShow")
def showcart():
    if(session.get("login") is None or session.get('login')== False ):
        return render_template("frontend/login.html")
    else:
         return render_template("frontend/cart.html")

@app.route("/cart/<id>")
def addtocart(id):
    data=ob.getdata("product","product_id",id)
    if( session.get('cart') is None):
        session['cart']=list()
    #it is append new item in Cart
    session['cart']= cart_ob.additem(data['data'][0],session['cart'])
    # it is calculate total amount in Cart
    session['total_amount']= cart_ob.cart_amount(session['cart'])
    #it is count how many item in Cart
    session['count']= cart_ob.count_item(session['cart'])
    return redirect(url_for("cart"))

@app.route("/UndoCart")
def undocart():
    if(session['count']>=1):
        session['cart']=cart_ob.cart_undo(session['cart'])
        session['total_amount']= cart_ob.cart_amount(session['cart'])
        #it is count how many item in Cart
        session['count']= cart_ob.count_item(session['cart'])
    return render_template("frontend/cart.html")

@app.route("/DelCart")
def Deletecart():
    session['cart']=cart_ob.cart_clear(session['cart'])
    session['total_amount']= cart_ob.cart_amount(session['cart'])
    #it is count how many item in Cart
    session['count']= cart_ob.count_item(session['cart'])
    return render_template("frontend/cart.html")

@app.route("/del/<id>")
def deletesinglerow(id):
    session['cart'] , ct =cart_ob.cart_del(id,session['cart'])
    session['count']=ct
    return render_template("frontend/cart.html")


@app.route("/login", methods=['GET','POST'])
def login2():
    error={}
    if request.method=="POST":
        email=request.form['xuser']
        password=request.form['xpass']
        condition=" where (email='" + email + "' or mobile='" + email + "') and  password ='" + password + "')"
        condition={"email":email,"password":password}
        data=ob.getalldata("customer",condition)
        if(data['count']>=1):
            lst=ob.getdata("customer","email",email)
            session['userid']=lst['data'][0][0]
            session['username']=lst['data'][0][1]
            session['email']=lst['data'][0][2]
            session['mobile']=lst['data'][0][4]
            session['city']=lst['data'][0][5]
            session['state']=lst['data'][0][6]
            session['login']=True
            return redirect(url_for("home"))
            if request.form['xrem'] is not None:
                resp = make_response(render_template('frontend/home.html'))
                resp.set_cookie('email', email,60*60*24)
                return resp
            else:
                return render_template("frontend/home.html")
        else:
            error="E-mail and password does not match"
    return render_template("frontend/login.html",err=error)

@app.route("/logout_customer")
def logout2():
        session.pop('username',"None")
        session.pop('email',"None")
        session['login']=False
        return redirect(url_for("home"))



@app.route("/registration")
def register():
    return render_template("frontend/registration.html")

@app.route("/register", methods=['GET','POST'])
def reg():
    error=""
    if request.method=="POST":
        username=request.form['xname']
        email=request.form['xmail']
        password=request.form['xpass']
        mobile=request.form['xmob']
        city=request.form['xcity']
        state=request.form['xstate']
        data={"name":username,"email":email,"Password":password,"mobile":mobile,"city":city,"state":state}
        data=ob.insert("customer",data)
    return render_template("frontend/registration.html")

@app.route("/cate/<id>")
def category1(id):
    data=ob.getdata("product","cat_id",id)
    return render_template('/frontend/industrial.html',err=data)

@app.route("/payment")
def paymentCart():
    if(session.get("login") is None or session.get('login')== False ):
        return render_template("frontend/login.html")
    else:
         return render_template("frontend/shipping.html")

@app.route("/popular/<int:id>//<int:val>")
def popular(id, val):
    if(val==0):
        rr=ob.update("product",{"popular":1},"product_id",id)
    else:
        rr=ob.update("product",{"popular":0},"product_id",id)

    return str(val)
    
# check karo