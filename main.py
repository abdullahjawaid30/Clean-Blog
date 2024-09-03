from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json


with open("config.json",'r') as c:
    params=json.load(c)["params"]
    
local_server=True 
    
app = Flask(__name__)
if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']
    
db = SQLAlchemy(app)

class Contacts(db.Model):
    __tablename__ = 'contact'  # Use the actual table name in the database
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=True)
    date = db.Column(db.String(12), nullable=False)
    
    

@app.route("/")
def home():
    return render_template('index.html',params=params)

@app.route("/about")
def about():
    return render_template('about.html',params=params)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, email=email, phone_number=phone, msg=message ,date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html',params=params)

@app.route("/post/<string:post_slug>",methods=['GET'])
def post():
    return render_template('post.html',params=params)

app.run(debug=True)
