import os, sys
'''
> python --version
> pip --version					(python.exe -m pip install --upgrade pip)
> python -m venv myworld		(must activate virtual environment every time you open command prompt)
> python -m pip install Django	(pip show Django)
> pip install psycopg2-binary
> django-admin --version		(5.2.7)

(NEW PROJECT in \notebooks\)
> django-admin startproject my_project
> cd my_project
> python manage.py runserver
(goto browser)
http://localhost:8000/

(NEW APP in \notebooks\my_project)
> cd my_project
> python manage.py startapp startup

(START)
> cd my_project
> python manage.py runserver
http://localhost:8000/
'''
print(f'sys.version: {sys.version}')
print(f'sys.version_info: {sys.version_info}')
print(f'os.getenv("USERNAME"): {os.getenv('USERNAME')}')

