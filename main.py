from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:enterbab@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(500))
    author_id = db.Column(db.String(120))

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.author_id = author_id

# TODO: #landing page redirected to blog
@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/blog')

# TODO:redirected from / showing all blogs
@app.route('/blog', methods=['POST', 'GET'])
def all_blog():
    blogs = Blog.query.all()
    return render_template('blog.html', title='Your Blog', blogs = blogs)

# TODO: query all blogs and return/gets the selected blog
def selected_blog():
    blog_id = request.args.get('id')
    blog_post = Blog.query.filter_by(blog_id).first()
    return render_template('selected_blog.html', title='Selected Blog' , blogs = blogs)

# TODO: new post and check for errors
@app.route('/newpost', methods=['POST','GET'])
def new_blog():
    #currently no errors
    title_error = ''
    content_error = ''

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['content']
        new_post = Blog(title=blog_title,content=blog_content)

    # TODO: no title error send to newpost
    elif blog_title == "":
        title_error = 'Eh...Try Again'
        return render_template('newpost.html', title_error=title_error)

    # TODO: no content error send to newpost
    elif blog_content == "":
        content_error = 'Write something!'
        return render_template('newpost.html', content_error=content_error)

    # TODO:redirect to blog
    else:
        db.session.add(new_blog)
        db.session.commit()
        new_blog = str(blog_title, blog_content)
    return render_template('newpost.html', title='New Blog')

if __name__ == '__main__':
    app.run()
