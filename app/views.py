from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Mario' }
    posts = [
        { 
            'author': { 'nickname': 'Arrow' }, 
            'body': 'Mario Rodolfo is Oliver Queen!' 
        },
        
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)
