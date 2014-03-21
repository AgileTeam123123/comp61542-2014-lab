from flask import Flask
import os

JQUERY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), './jquery')
print(JQUERY_DIR)
app = Flask(__name__,static_folder=JQUERY_DIR)

from comp61542 import views
