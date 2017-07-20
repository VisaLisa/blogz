from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

#TODO import os deplaying with heroku

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:enter@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#app.secret_key = ''


class Blogz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1500))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, content, author, pub_date):
        self.title = title
        self.content = content
        self.author = author
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(20))
    posts = db.relationship('Blogz', backref='author')

    def__init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request():
def req_login():
    allowed_routes = ['login', 'signup', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

#TODO logout.html ; We'll have a logout function that handles a POST request to /logout and redirects the user to /blog after deleting the username from the session
@app.route('/logout', methods=['POST'])
def logout():
    del session['username']
    return redirect('/blog')

#TODO signup.html
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_pw = request.form['verify_pw']
        existing_user = User.query.filter_by(username=username).first()
        error_signup = False

    #TODO: validate user's data and/or return error
    if not username == "" or password == "" or verify_pw == "":
        flash ("Your Username and/or Password is invalid")
        error_signup = True
    if not verify_length(username):
        flash("Your username should be between 5 and 20 characters.")
        error_signup = True
    if not verify_length(password):
        flash("Your password should be between 5 and 20 characters.")
        error_signup = True
    if not password != verify_pw:
        flash("Your passwords don't match - Please try again.")
        error_signup = True
    if not existing_user:
        flash("The username your are trying to use it already taken - Please try again.")
        error_signup = True
    if not error_signup == True:
        return render_template("/signup.html", title="Sign Up", username=username)

    #TODO: adding new user to the database
    if not  existing_user and password == verify_pw:
        new_user =User(username, password)
        db.session.add(new_user)
        db.session.commit()
        session['username']=username
        return redirect('/login')

    return render_template("/signup.html", title="Sign Up")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("You're logged in!")
            return redirect('/newpost')
        elif user == None:
            flash('Username and/or password is incorrect - Try again.')
            return redirect('/login')
        elif user.password != password:
            flash("Your password does not match - Try again")
            return redirect('/login')

    return render_template('login.html', title="Log in", username=username)


#TODO: singleUser.html template that will be used to display only the blogs associated with a single given author. It will be used when we dynamically generate a page using a GET request with a user query parameter on the /blog route (similar to how we dynamically generated individual blog entry pages in the last assignment)
@app.route('/singleUser', methods=['GET'])
def display_user_post():
    user_post =

# TODO: index.html
@app.route('/', methods=['POST', 'GET'])
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/blog', methods=['GET'])
def blog():
    blogs = Blogz.query.all()
    return render_template('blog.html', title='Your Blog', blogs=blogs)

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
        username = session['username']

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
        elif:
        new_blog = Blogz(blog_title, blog_content, username)
        db.session.add(new_blog)
        db.session.commit()
        blog_id = str(new_blog.id)
        return redirect('/blog?id=' + str(blog_id))

    if request.method == 'GET':
    return render_template('newpost.html')




if __name__ == '__main__':
    app.run()
