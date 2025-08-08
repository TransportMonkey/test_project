import typing

from model.user import User
from services.user import view_model as vm
from .base_ctl import BaseCtl
from common import logmode
from werkzeug.exceptions import BadRequest


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

