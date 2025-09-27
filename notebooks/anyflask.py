# > pip install Flask
# > flask --app anyflask run --debug

import datetime

from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)
timestamp = datetime.datetime.now().isoformat()


@app.route("/", methods=['POST', 'GET'])
def root(name=None):
	print('root')
	assert request.path == '/'
	return render_template('anyflask.html', timestamp=timestamp, person=name)

@app.route('/user/<username>')
def show_user_profile(username):
	return f'User {escape(username)}'

@app.route('/post/<int:post_id>')
def show_post(post_id):
	return f'Post {post_id}'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
	return f'Subpath {escape(subpath)}'

print(f'█▓▒░ START APP ░▒▓█\n{timestamp}')
