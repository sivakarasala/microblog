from flask import render_template
# app - package, app - object of Flask class instance
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'visweswaraya'}
    posts = [
        {
            'author': {'username': 'Mahadevaya'},
            'body': 'Om Mahadevaya Namaha'
        },
        {
            'author': {'username': 'Tryambakaya'},
            'body': 'Om Tryambakaya Namaha'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
