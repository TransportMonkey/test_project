from model.user import User
from services.user import view_model as vm
from . import api
from flask_pydantic import validate
from controls.user import UserCtl
from common.web import AdvResource
from flask import request
# from common.view_model import PageReq


@api.route('/')
class UsersView(AdvResource):
    model = User
    control = UserCtl

    exclude_fields = ["password"]

    # @api.expect(PageReq.rest_x_model(api))
    # @validate(query=PageReq)
    def get(self):
        """查看用户列表"""

        return self.get_page(request)

    @api.expect(vm.UserCreateOrPutReq.rest_x_model(api))
    @validate()
    def post(self, body: vm.UserCreateOrPutReq):
        """创建用户"""
        user = self.control.create(body)
        return user.to_dict(exclude_fields=self.exclude_fields)


@api.route('/<int:user_id>/')
class UserView(AdvResource):
    model = User
    control = UserCtl
    exclude_fields = ["password"]

    def get(self, user_id):
        """查看单个用户"""
        user = self.model.find_or_fail(user_id)

        return user.to_dict(exclude_fields=self.exclude_fields)

    @api.expect(vm.UserCreateOrPutReq.rest_x_model(api))
    @validate()
    def put(self, user_id, body: vm.UserCreateOrPutReq):
        """完整更新用户"""
        ctl = self.control.new_by_id(user_id)
        user = ctl.update(body)
        return user.to_dict(exclude=self.exclude_fields)

    @api.expect(vm.UserPatchReq.rest_x_model(api))
    @validate()
    def patch(self, user_id, body: vm.UserPatchReq):
        """部分更新用户"""
        ctl = self.control.new_by_id(user_id)
        user = ctl.update(body)
        return user.to_dict(exclude=self.exclude_fields)

    def delete(self, user_id):
        """删除用户"""
        ctl = self.control.new_by_id(user_id)
        return ctl.simple_delete()
