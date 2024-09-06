from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json

with open("config.json", 'r') as c:
    params = json.load(c)["params"]
    print(params)  # This will print in your Flask console

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
    

class Posts(db.Model):
    __tablename__ = 'post'  # Use the actual table name in the database
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=False)
    img_file = db.Column(db.String(12), nullable=False)
    
   

@app.route("/")
def home():
    posts = Posts.query.filter_by().all()[0:params['no_of_Posts']]
    return render_template('index.html', params=params, posts=posts)




@app.route("/dashboard")
def dashboard():
    return render_template('login.html', params=params)


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




@app.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    if post is None:
        return "Post not found", 404
    return render_template('post.html', params=params, post=post)





app.run(debug=True)
