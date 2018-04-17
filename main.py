from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:squeesquee@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asdfghjkl'


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

    def __repr__(self):
        return self.title

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    blogs = db.relationship('Blog', backref='owner ')

    def __init__(self,username,password):
        self.username = username
        self.password = password

@app.route('/blog', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.all()
    blog_id = request.args.get('id')

    if request.method == 'GET' and request.args.get('id'):
        single_blog = Blog.query.filter_by(id=blog_id).first()
        return render_template('blog-post.html', single_blog=single_blog)
    else:
        return render_template('blog.html', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():
    if request.method == 'POST':
        newpost_name = request.form['np-title']
        newpost_body = request.form['np-body']
        title_error = "Please specify the title of your post."
        body_error = "Please add something to the body."
        if newpost_name.strip() == "" and newpost_body.strip() == "":
            return render_template("newpost.html", title_error=title_error, body_error=body_error)
        if newpost_name.strip() == "":
            return render_template("newpost.html", title_error=title_error)
        if newpost_body.strip() == "":
            return render_template("newpost.html", body_error=body_error)

        newpost = Blog(newpost_name,newpost_body)
        db.session.add(newpost)
        db.session.commit()

        blog_id = newpost.id
        blog_id = str(blog_id)
        return redirect('/blog?id=' + blog_id)
        
    return render_template('newpost.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        #TODO validate user data

        #Checks to see the username is already in use
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:                       #If the username isn't in use we commit the
            new_user = User(username, password)     #validated data into the db, and add the username
            db.session.add(new_user)                #into the session.
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        else:
            #TODO better response message
            return '<h1>YOU ALREADY EXIST</h1>'


    return render_template('signup.html')
#@app.route('/login')
#@app.route('/index')
#@app.route('/logout')

if __name__ == '__main__':
    app.run()