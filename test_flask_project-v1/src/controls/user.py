import typing,secrets
from datetime import datetime, timedelta
from model.user import User,Token
from services.user import view_model as vm
from .base_ctl import BaseCtl
from common import logmode
from werkzeug.exceptions import BadRequest
from flask import current_app


class UserCtl(BaseCtl):
    model_cls = User

    @property
    def user(self) -> User:
        return self.model

    @classmethod
    def exist_user_name(cls, name: str):
        return cls.model_cls.where(name=name).first() is not None

    @classmethod
    def create(cls, args: vm.UserCreateOrPutReq) -> User:
        logmode.info("create user args %s", args)
        if cls.exist_user_name(args.name):
            raise BadRequest("用户名已注册，请更换名字再重试")
        return cls.model_cls.create(**args.model_dump(exclude_none=True))

    def update(self, args: typing.Union[vm.UserCreateOrPutReq, vm.UserPatchReq]):
        """更新用户"""
        args = args.model_dump(exclude_none=True)
        if len(args) > 0:
            if "name" in args and args["name"] != self.user.name and self.exist_user_name(args["name"]):
                raise BadRequest("用户名已注册，请更换名字再重试")
            logmode.info("update user[%s-%s] args %s", self.user.id, self.user.name, args)
            self.user.update(**args)
        return self.user

    def delete(self):
        # 删除_id
        for todo in self.user.todos:
            todo.delete()
        for token in self.user.tokens:
            token.delete()
        # 删除id
        self.user.delete()

class TokenCtl(BaseCtl):
    model_cls = Token

    @property
    def login(self) -> Token:
        return self.model

    @classmethod
    def create(cls, user_name, user_pwd):
        user = User.where(name=user_name).first()
        if user:
            if user.password == user_pwd:
                token = cls.model_cls.query.filter(cls.model_cls.user_id==user.id).order_by(cls.model_cls.id.desc()).first()
                if not token:
                    args = cls.insert_data(user.id)
                    cls.model_cls.create(**args)
                    return args['token']
                else:
                    if datetime.now() >= token.expire_time:
                        args = cls.insert_data(user.id)
                        cls.model_cls.create(**args)
                        return args['token']
                    else:
                        return token.token
            raise BadRequest('密码错误！')
        raise BadRequest('用户不存在！')


    @classmethod
    def insert_data(cls, user_id)->dict:
        hours = current_app.get_config("EXPIRED_TIME",24)
        args = {'token': secrets.token_urlsafe(11),
                'user_id': user_id,
                'expire_time': datetime.now() + timedelta(hours=hours)
                }
        return args







