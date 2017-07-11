from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

#TODO import os deplaying with heroku

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:enter@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blogz(db.Model):
    id = db.Column(db.Integer, primary_key=True, AUTO_INCREMENT)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1500))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.author = author

#TODO add user class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, AUTO_INCREMENT)
    username = db.Column(db.String(15))
    password = db.Column(db.String(20))
    posts = db.relationship('Blogz', backref='author')

    def__init__(self, username, password):
        self.username = username
        self.password = password

#TODO login.html
@app.before_request
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("You're logged in!")
            return redirect('/blog')
        else:
            flash('Username and/or password is incorrect, Try again')

    return render_template('login.html')


#TODO signup.html
@app.route('/signup')


#TODO index.html
@app.route('/index')

#TODO logout.html ; We'll have a logout function that handles a POST request to /logout and redirects the user to /blog after deleting the username from the session
@app.route('/logout', methods=['POST'])
def logout():
    del session['email']
    return redirect('/blog')

#TODO: singleUser.html template that will be used to display only the blogs associated with a single given author. It will be used when we dynamically generate a page using a GET request with a user query parameter on the /blog route (similar to how we dynamically generated individual blog entry pages in the last assignment)
@app.route('/singleUser', methods=['GET'])
def display_user_post():
    user_post =

# TODO: landing page redirected to blog
@app.route('/')
def index():
    return redirect('/blog')

# TODO: redirected from / showing all blogs
@app.route('/blog', methods=['GET'])
def blog():
    blogs = Blogz.query.all()
    return render_template('blog.html', title='Your Blog', blogs=blogs)


# TODO: query all blogs and return/gets the selected blog
@app.route('/selected_blog', methods=['GET'])
def selected_blog():
    blog_id = request.args.get('id')
    blog_post = Blogz.query.filter_by(id=blog_id).first()
    return render_template('selected_blog.html', selected_blog=blog_post)


# TODO: new post and check for errors
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    # currently no errors
    title_error = ''
    content_error = ''
    error_check = False

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']

        # no title error send to newpost
        if not blog_title:
            title_error = 'Eh...Try Again'
            error_check = True

            # no content error send to newpost
        if not blog_content:
            content_error = 'Write something!'
            error_check = True

            # redirect to blog
        if error_check:
            return render_template('newpost.html', title_error=title_error, content_error=content_error)

        new_blog = Blogz(blog_title, blog_content)
        db.session.add(new_blog)
        db.session.commit()
        blog_id = str(new_blog.id)
        return redirect("/blog?id=" + blog_id)
    return render_template('newpost.html')




if __name__ == '__main__':
    app.run()
