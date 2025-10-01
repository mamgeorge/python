# > pip install Flask
# > flask --app anyflask run --debug
# http://localhost:5000/

import datetime

from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)
timestamp = datetime.datetime.now().isoformat()

@app.route("/", methods=['POST', 'GET'])
def root(name=None):
	print(f'root is running on: {request.host_url}')
	assert request.path == '/'
	return render_template('anyflask.html',
		timestamp=datetime.datetime.now().isoformat(),
		link=request.host_url, person=name)

@app.route('/user/<username>')
def show_user_profile(username):
	return render_template('details.html', value=username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
	return render_template('details.html', value=post_id)

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
	return render_template('details.html', value=escape(subpath))

print(f'█▓▒░ START APP ░▒▓█\n{timestamp}')
