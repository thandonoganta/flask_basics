from flask import Flask, request, render_template, session,g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd


app = Flask(__name__)

app.config.update(

    SECRET_KEY = 'PanxuPanxu7671$'

    ,SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:PanxuPanxu7671$@localhost/catalog_db'

    ,SQLALCHEMY_TRACK_MODIFICATIONS=False

)

db = SQLAlchemy(app)

# Before Requests
@app.before_request
def some_function():
    g.string = '<br> This code ran before my request'


# Hello  World
@app.route('/')
def hello_flask():
    return 'Hello Flask! <br>' + g.string

# Using query strings
@app.route('/new/')
def query_strings(greeting = 'Molo'):
    query_val = request.args.get('greeting', greeting)
    return '<h1> The greeting is : {0} </h1>'.format(query_val) + g.string


# getting rid of query strings
@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='Panxu'):
    return '<h1> Hello There : {} </h1>'.format(name)

# Data type 1: strings
@app.route('/text/<string:num>')
def working_with_strings(num):
    return '<h1> The number you picked is : ' + num + '</h1>'

# Data type1: strings again
@app.route('/numbers/<int:num>')
def working_with_integers(num):
    return '<h1> The number you entered is : ' + str(num) + '</h1>'

# Data type2: integers
@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2):
    return '<h1> The sum is : {}'.format(num1 + num2) + '</h1>'

# Data type3: floats
@app.route('/product/<float:num1>/<float:num2>')
def product(num1, num2):
    return '<h1> The product is : {}'.format(num1 * num2) + '</h1>'

# Working with templates
@app.route('/temp')
def using_templates():
    return render_template('hello.html')

# Jinja Templates
@app.route('/watch')
def top_movies():
    movie_list = ['autopsy of jane doe'
                  ,'neon demon'
                  ,'ghost in a shell'
                  ,'kong: skull island'
                  ,'john wick 2'
                  ,'spiderman - homecoming']

    return render_template('movies.html'
                           ,movies = movie_list
                           ,name='Thando')


# Working with Tables
@app.route('/tables')
def movies_plus():
    movies_dict = {'autopsy of jane doe': 02.14
                    ,'neon demon': 3.29
                    , 'ghost in a shell': 1.5
                    , 'kong: skull island': 3.5
                    , 'john wick 2': 02.52
                    , 'spiderman - homecoming': 1.48}

    return render_template('table_data.html'
                           ,movies=movies_dict
                           ,name='Panxu')



# Filters in Jinja2
@app.route('/filters')
def filter_data():
    movies_dict = {'autopsy of jane doe': 02.14
                    ,'neon demon': 3.29
                    , 'ghost in a shell': 1.5
                    , 'kong: skull island': 3.5
                    , 'john wick 2': 02.52
                    , 'spiderman - homecoming': 1.48}

    return render_template('filter_data.html'
                           ,movies=movies_dict
                           ,name=None
                           ,film='a christmas carol')


# Working with Macros
@app.route('/macros')
def jinja_macros():
    movies_dict = {'autopsy of jane doe': 02.14
                    ,'neon demon': 3.29
                    , 'ghost in a shell': 1.5
                    , 'kong: skull island': 3.5
                    , 'john wick 2': 02.52
                    , 'spiderman - homecoming': 1.48}

    return render_template('using_macros.html', movies=movies_dict)

# Working with Session Object
@app.route('/session')
def session_data():
    if 'name' not in session:
        session['name'] = 'Thando'
    return render_template('session.html', session = session, name=session['name'])


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'The Publisher is {}'.format(self.name)


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # ESTABLISH RELATIONSHIP
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):
        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


# pd.set_option('display.expand_frame_repr', False)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
