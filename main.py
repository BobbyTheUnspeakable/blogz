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


@app.route('/blog', methods=['POST', 'GET'])
def index():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

#    if request.method == 'POST':
#        task_name = request.form['task']
#        new_task = Task(task_name)
#        db.session.add(new_task)
#        db.session.commit()

#    blogs = Blog.query.all()
#    completed_tasks = Task.query.filter_by(completed=True).all()
#    return render_template('todos.html',title="Get It Done!", 
#        tasks=tasks, completed_tasks=completed_tasks)


@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():

#    newpost_name = request.form['np-title']
#    newpost_body = request.form['np-body']

#    if (not newpost_name) or (newpost_name.strip() == ""):
#        error = "Please specify the movie you want to add."
#        return redirect("/?error=" + error)

#    newpost = Blog(newpost_name,newpost_body)
#    db.session.add(newpost)
#    db.session.commit()

    return render_template('newpost.html')#, newpost=newpost)

#    blog_id = int(request.form['blog-id'])
#    blog_post = Blog.query.get(blog_id)
#    task.completed = True
#    db.session.add(task)
#    db.session.commit()

#    return redirect('/')

#if __name__ == '__main__':
app.run()