from flask import Flask, render_template, request, session, make_response, url_for
from werkzeug.utils import redirect

from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

app = Flask(__name__)
# __name__ is a built in var for private variable which contains '__main__'
app.secret_key = 'TODO change this key later'


@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login')
def login_template():
    return render_template('login.html')


@app.route('/register')
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    # request.form is a dictionary with all data in the form
    email = request.form['email']  # using form --> input tag's name
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None
        # TODO unset the email, redirect to login page
        # show warning email is wrong
    # rendering a template with data
    return render_template('profile.html', email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    # request.form is a dictionary with all data in the form
    email = request.form['email']  # using form --> input tag's name
    password = request.form['password']

    User.register(email, password)
    # session['email'] = email

    return render_template('profile.html', email=session['email'])


@app.route('/blogs/<string:user_id>', methods=['GET'])
@app.route('/blogs', methods=['GET'])
def user_blogs(user_id=None):
    if request.method == 'POST':
        return redirect(url_for('user_blogs'))

    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()

    return render_template('user_blogs.html',
                           blogs=blogs,
                           email=user.email)


@app.route('/blogs/new', methods=['GET', 'POST'])
def create_new_blog():
    if request.method == 'POST':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])
        new_blog = Blog(author=user.email,
                        title=title,
                        description=description,
                        author_id=user._id)
        new_blog.save_to_mongo()

        # return render_template('user_blogs.html')
        # TODO: refreshing the page after created the blog will create another blog
        # TODO: investigate this issue
        # TODO: hitting enter reloads the list of blogs
        # redirected post request in user_blog
        return make_response(user_blogs(user._id))


@app.route('/posts/<string:blog_id>', methods=['GET'])
def blog_posts(blog_id):
    if request.method == 'POST':
        return redirect(url_for('blog_posts', blog_id=blog_id))
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()
    return render_template('posts.html',
                           posts=posts,
                           blog_title=blog.title,
                           blog_id=blog._id)


@app.route('/posts/new/<string:blog_id>', methods=['GET', 'POST'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_email(session['email'])
        new_post = Post(blog_id=blog_id,
                        title=title,
                        content=content,
                        author=user.email)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))


if __name__ == '__main__':
    app.run(debug=True, port=4995)

