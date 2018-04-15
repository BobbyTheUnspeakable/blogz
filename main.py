from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:squeesquee@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def __repr__(self):
        return self.title


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

if __name__ == '__main__':
    app.run()