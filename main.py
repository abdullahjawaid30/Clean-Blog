from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import json

# Load configuration
with open("config.json", 'r') as c:
    params = json.load(c)["params"]

local_server = params['local_server'] == "True"

app = Flask(__name__)
app.secret_key = 'beyondyourlife'
app.config['UPLOAD_FOLDER'] = params['upload_location']
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit to 16 MB

if local_server:
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

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    posts = Posts.query.all()[0:params['no_of_Posts']]
    return render_template('index.html', params=params, posts=posts)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    # Check if the user is already logged in
    if 'user' in session and session['user'] == params['admin_user']:
        # Fetch all posts from the database
        posts = Posts.query.all()
        return render_template('dashboard.html', params=params, posts=posts)
    
    # If not logged in, handle login POST request
    if request.method == "POST":
        # Get the login details
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        
        # Check if the credentials are correct
        if username == params['admin_user'] and userpass == params['admin_password']:
            # Set the session variable for user
            session['user'] = username
            # Fetch all posts from the database
            posts = Posts.query.all()
            return render_template('dashboard.html', params=params, posts=posts)
        else:
            # If credentials are wrong, show login page again
            return render_template('login.html', params=params)
    
    # If the request method is GET, show the login page
    return render_template('login.html', params=params)

@app.route("/edit/<string:sno>", methods=['GET', 'POST'])
def edit(sno):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == "POST":
            # Get form data
            editTitle = request.form.get('editTitle')
            editLine = request.form.get('editLine')
            editSlug = request.form.get('editSlug')
            editContent = request.form.get('editContent')
            editImg_file = request.form.get('editImg_file')
            date = datetime.now()
            
            if sno == '0':
                # New post
                newPost = Posts(title=editTitle, content=editContent, slug=editSlug, tagline=editLine, img_file=editImg_file, date=date)
                db.session.add(newPost)
                db.session.commit()
            else:
                # Update existing post
                post = Posts.query.filter_by(sno=sno).first()
                post.title = editTitle
                post.content = editContent
                post.slug = editSlug
                post.tagline = editLine
                post.img_file = editImg_file
                post.date = date
                db.session.commit()
            return redirect('/dashboard')  # Redirect after saving
        
        # Fetch the post to be edited
        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, post=post, sno=sno)

@app.route("/uploader", methods=['POST'])
def uploader():
    if "user" in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            if 'file1' not in request.files:
                return "No file part", 400
            file = request.files['file1']
            if file.filename == '':
                return "No selected file", 400
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect('/dashboard')  # Redirect back to dashboard
    return redirect('/')


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect("/dashboard")


@app.route("/about")
def about():
    return render_template('about.html', params=params)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, email=email, phone_number=phone, msg=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)

@app.route("/post/<string:post_slug>", methods=['GET'])
def post(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    if post is None:
        return "Post not found", 404
    return render_template('post.html', params=params, post=post)

if __name__ == "__main__":
    app.run(debug=True)
