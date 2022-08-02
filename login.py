from flask import Flask, request, render_template,url_for
from flask_session import Session
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from library import *
import requests



app = Flask(__name__)
ob=library()
app.secret_key = 'kjfhdskjfh sfkjshd'

#email configration code
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dimplesotwal@gmail.com'
app.config['MAIL_PASSWORD'] = '8094608129'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)