'''
	had to install venv first
	colorterm works with UTF-8 if run configuration is updated to run as terminal console
	pip install termcolor
'''
import os, sys, platform
from datetime import datetime
from termcolor import colored
import sqlite3
import requests
import json
from jsonpath_ng.ext import parse

EOL = os.linesep

def tempSys():

	dateTime = datetime.now().isoformat()
	print(colored('-' * 40, 'green'))
	print(f"dateTime: {dateTime}")
	print(f'datetime.now().isoformat(): {datetime.now().isoformat()}')

	print(colored('-'*40, 'blue'))
	print(f'sys.version: {sys.version}')
	print(f'sys.getdefaultencoding: {sys.getdefaultencoding()}')
	print(f'platform.python_version(): {platform.python_version()}')

	print(colored('-'*40, 'blue'))
	try:
		filePath = 'notes.md'
		with open(filePath, 'r', encoding='utf-8') as file:
			content = file.read()
			print(content[0:10])
	except FileNotFoundError:
		print(f"ERROR: The file '{filePath}' was not found.")

	print(colored('-' * 40, 'blue'))
	# ░ ▒ ▓ █ ▄ ▀ ▌ ▐ ▬ ■ ─ ═ ► ◄ ▲ ▼ √ • ↨ ↔︎ ↑ ↓ → ← ┼ ╬
	colors = 'red yellow green cyan blue magenta white black'.split()
	[print(colored('░', color, attrs=['bold']), end='') for color in colors]
	print(EOL)

def tempDBs():

	print(colored('-' * 40, 'green'))
	dbFile = 'C:/workspace/dbase/sqlite/chinook.db'
	SQL_LIST = 'SELECT * FROM customers WHERE company != \'\' ORDER BY customerId ASC;'
	try:
		with sqlite3.connect(dbFile) as conn:

			cursor = conn.cursor()
			cursor.execute(SQL_LIST)
			rows = cursor.fetchall()

	except sqlite3.Error as ex:
		print(f"An SQLite error occurred: {ex}")
	except Exception as ex:
		print(f"An unexpected error occurred: {ex}")

	ictr = 0
	for row in rows:
		ictr += 1
		print(f'  {ictr:02d} {(row[1] + ' ' + row[2]):<25} {('| ' + row[7])}')

	print('')

def tempHttp():

	print(colored('-' * 40, 'green'))
	url = "https://jsonplaceholder.typicode.com/posts/1"
	response = requests.get(url)
	if response.status_code == 200:
		print("Request successful!")
		print(response.json())
	else:
		print(f"Request failed with status code: {response.status_code}")

def tempJson():

	print(colored('-' * 40, 'green'))
	json_data = {
		"store": {
			"book": [
				{"category": "reference", "author": "Nigel Rees"		, "title": "Sayings of the Century"	, "price": 8.95 },
				{"category": "fiction"	, "author": "Evelyn Waugh"		, "title": "Sword of Honour"		, "price": 12.99 },
				{"category": "fiction"	, "author": "Herman Melville"	, "title": "Moby Dick"				, "isbn": "0-553-21311-3", "price": 7.99 },
				{"category": "fiction"	, "author": "J.R.R. Tolkien"	, "title": "The Lord of the Rings"	, "isbn": "0-345-33970-3", "price": 22.99 }
			],
			"bicycle": {
				"color": "red",
				"price": 19.95
			}
		}
	}
	# PARSE REQUIRES DICTIONARY JSON!
	json_author = parse('$.store.book[*].author')
	match_body = json_author.find(json_data)
	print(f'author reads: {match_body[0].value}')

	json_authors = parse('$.store.book[?(@.price > 10)].author')
	json_booklist = [match.value for match in json_authors.find(json_data)]
	print(f'Authors: {json_booklist}')

print("Hello, World!" )

tempSys()
tempDBs()
tempHttp()
tempJson()

