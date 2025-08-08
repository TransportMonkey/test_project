from flask_restx import Namespace

api = Namespace("todo")

from . import views
