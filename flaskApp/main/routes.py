import os

from flask import Blueprint, render_template, flash, send_from_directory
from flask_login import login_required

from flaskApp.models import Post, Upload

main = Blueprint('main',__name__)


@main.route('/')
def home():
    return render_template('home.html')

@main.route('/profile')
@login_required
def profile():


    flash('Please verify your account')
    return render_template('USER_BASE.html')




@main.route('/event')
def event():
    return render_template('EVENTS.html')

@main.route('/consult')
def consult():
    all_posts = Post.query.all()

    return render_template('CONSULT.html',all_posts=all_posts)

@main.route('/unitalk')
def unitalk():
    return render_template('UNITALK.html')

@main.route('/about')
def about():
    return render_template('ABOUT.html')


@main.route('/coronavirus')
def corona():
    return render_template('corona.html')

@main.route('/discover_h', defaults={'req_path': ''})
@main.route('/<path:req_path>')
def discover_h(req_path):

    # Permission

    BASE_DIR = '/Users/ASUS/Desktop/100CHINAGUIDE/flaskApp/static'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return os.abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_from_directory(abs_path)

    # Show directory contents
    upload = os.listdir(abs_path)
    uploads = Upload.query.all()


    print(upload)
#    uploads = send_from_directory(directory='videos',filename='videos')
    return render_template('discover_h.html',uploads=uploads)