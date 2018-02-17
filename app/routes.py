# app - package, app - object of Flask class instance
from app import app

@app.route('/')
@app.route('/index')
def index():
    return 'Om Namah Shivaya'
