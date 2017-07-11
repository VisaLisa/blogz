from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:enterbab@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1500))

    def __init__(self, title, content):
        self.title = title
        self.content = content

# TODO: #landing page redirected to blog
@app.route('/')
def index():
    return redirect('/blog')

# TODO:redirected from / showing all blogs
@app.route('/blog', methods=['GET'])
def blog():
    blog = Blog.query.all()
    print(blogs[0].title)
    return render_template('blog.html', title='Your Blog')

# TODO: query all blogs and return/gets the selected blog
@app.route('/selected_blog', methods=['GET'])
def selected_blog():
    blog_id = request.args.get('id')
    blog_post = Blog.query.filter_by(id=blog_id).all()
    print(blog_post[0].title) #query as a list
    return render_template('selected_blog.html', selected_blog=blog_post[0])

# TODO: new post and check for errors
@app.route('/newpost', methods=['POST','GET'])
def new_blog():
    #currently no errors
    title_error = ''
    content_error = ''
    error_check = False

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']

    # TODO: no title error send to newpost
        if blog_title == '':
            title_error = 'Eh...Try Again'
            error_check = True

    # TODO: no content error send to newpost
        if blog_content == '':
            content_error = 'Write something!'
            error_check = True

    # TODO:redirect to blog
        if error_check == True:
            return render_template('newpost.html', title_error=title_error, content_error=content_error)

        new_blog = Blog(blog_title,blog_content)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/selected_blog?id={{blog_id}}')
    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()
