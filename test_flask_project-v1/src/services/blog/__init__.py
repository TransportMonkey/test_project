from flask_restx import Namespace

api = Namespace("blog")

from . import views
