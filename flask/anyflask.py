# ( .\.venv\Scripts\activate )
# > pip install Flask flask_sqlalchemy SQLAlchemy flask_moment Moment
# > pip install psycopg2-binary
# > flask --app anyflask run --debug
# http://localhost:5000/

import datetime

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from markupsafe import escape
from anyconn import DB_URLSTRING

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URLSTRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended to suppress warnings
db = SQLAlchemy(app)
moment = Moment(app)

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
	return render_template('process.html', value=username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
	return render_template('process.html', value=post_id)

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
	return render_template('process.html', value=escape(subpath))

@app.route('/lister')
def show_lister():

	msg = 'AWS RDS PostgreSQL SUCCESS!'
	tabledata = None
	try:
		SQL = 'SELECT version();'
		val = db.session.execute(db.text(SQL))
		print(f'val: {val}')
		rows = Member.query.all()
		tabledata = [{
			'firstname'		: row.firstname,
			'lastname'		: row.lastname,
			'phone'			: row.phone,
			'joined_date'	: row.joined_date,
		} for row in rows]
		print(f'rows: {len(rows)}')

	except Exception as ex:
		msg = f'ERROR AWS RDS PostgreSQL connection: {ex}'
		print(f'msg: {msg}')

	return render_template('lister.html', value=msg, data=rows)

@app.route('/details/<item>')
def show_details(item):

	print('-' * 80)
	msg = 'AWS RDS PostgreSQL SUCCESS!'
	object = None
	try:
		SQL = 'SELECT version();'
		val = db.session.execute(db.text(SQL))
		print(f'val: {val}')
		object = Member.query.get(item)
		print(f'item: {item}, object: {object}')

	except Exception as ex:
		msg = f'ERROR AWS RDS PostgreSQL connection: {ex}'
		print(f'msg: {msg}')

	return render_template('details.html', value=msg, data=object)

print(f'█▓▒░ START APP ░▒▓█\n{timestamp}\n{DB_URLSTRING}')

class Member(db.Model):

	__tablename__ = 'startup_member'
	firstname	= db.Column(db.String(255)	, primary_key=True)
	lastname	= db.Column(db.String(255)	)
	phone		= db.Column(db.Integer		, nullable=True)
	joined_date	= db.Column(db.DateTime		, nullable=True, default=datetime.datetime.utcnow)

	def __repr__(self):
		return f'<Member {self.firstname}>'