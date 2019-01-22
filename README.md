to run the project
==================
####have `python` (>=2.7), `pip` and `virtualenv` installed    


      $ git clone https://github.com/gdzhu/db_project_weather.git
      $ cd db_project_weather/mysite/src/
      $ virtualenv venv
      $ . venv/bin/activate
      $ pip install -r requirements.txt
      $ python manage.py syncdb
      $ python manage.py runserver


