#!/usr/bin/python
activate_this = '/stud/jel048/public_html/flask_app/flask_app/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/stud/jel048/public_html/flask_app/")
sys.path.insert(1,"/stud/jel048/public_html/flask_app/flask_app/")

from flask_app import app as application