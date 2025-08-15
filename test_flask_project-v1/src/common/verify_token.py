from datetime import datetime
from flask import request
from model.user import User,Token
import typing
from functools import wraps
from werkzeug.exceptions import Unauthorized,Forbidden


def get_request_user()->typing.Optional[User]:
    if hasattr(request, "user"):
        return request.user
    return None

def get_user_token()->typing.Optional[Token]:
    if hasattr(request, "token"):
        return request.token
    return None


def require_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('TOKEN')
        if not token:
            raise Unauthorized('Token is missing!')
        login_token = Token.query.filter_by(token=token).first()
        if not login_token:
            raise Forbidden('Token is invalid or expired!')
        if datetime.now() >= login_token.expire_time:
            raise Forbidden('Token is expired!')
        user = login_token.user
        setattr(request, 'user', user) # 动态设置属性
        setattr(request, 'token', login_token)
        return f(*args, **kwargs)
    return decorated_function