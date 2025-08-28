from flask_restx import Namespace

api = Namespace("course")

from . import views