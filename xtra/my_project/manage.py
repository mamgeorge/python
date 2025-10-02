#!/usr/bin/env python
import os, sys, datetime

def main():

	print(f'█▓▒░ START ISO: {datetime.datetime.now().isoformat()}')
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
	try:
		from django.core.management import execute_from_command_line
	except ImportError as ex:
		msg = 'Django not imported. Is it installed? on PYTHONPATH env var? is VENV activated?'
		raise ImportError(msg) from ex
	execute_from_command_line(sys.argv)
	print(f'█▓▒░ DONE')

if __name__ == '__main__':
	main()
