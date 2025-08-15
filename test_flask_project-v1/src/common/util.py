from flask import current_app
from flask_mail import Mail


def get_email()->Mail:
    return current_app.mail

def get_config(key:str, default_value=0):
    result = current_app.get_config(key, default_value)
    return result
