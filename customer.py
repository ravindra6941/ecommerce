from flask import Flask, render_template, redirect, url_for, request,session
from __main__ import app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from library import *
from Cartlib import *


ob=library()
cart_ob=Cart()

# @app.route("/customerportal")
# def customer_portal():
#     session['customerdata']=ob.getdata("customer","id",str(session['username']))
#     session['orderdata']=ob.getdata("myorder","customer_id", str(session['userid']))
#     return render_template("customer/portal.html")

# @app.route("/Order")
# def order():
#     return render_template("customer/order.html")