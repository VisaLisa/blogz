from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer(11))
    date_posted = db.Column(db.DateTime)

    def __init__(self, title, post, author_id, date_posted = None):
        self.title = title
        self.content = content
        self.author_id = author_id
        if date_posted is None:
            date_posted = datetime.utcnow()
        self.date_posted = date_posted

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    name = request.form['name']
    entry = request.form['entry']
    error = ''
    if name == '' or entry == '':
        error = 'Please enter text'
        return render_template('newpost.html', error=error)
    else:
        new_post = Blog(name,entry)
        db.session.add(new_post)
        db.session.commit()


@app.route('/blog', methods=['POST', 'GET'])
def blogposts():
    blogs = Blog.query.all()
    return render_template('blog.html',title=title,
        name=name , body=body)





if __name__ == '__main__':
    app.run()
