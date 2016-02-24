import os, sys

project_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(project_path)
sys.path.append(project_path)

from config import VENV_PATH
activate_this = VENV_PATH + '/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

print(sys.version)

from app import app as application
