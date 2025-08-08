from flask_restx import Namespace

api = Namespace("user")

from . import views
