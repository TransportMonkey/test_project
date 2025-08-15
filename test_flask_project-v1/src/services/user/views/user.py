from model.user import User
from services.user import view_model as vm
from services.user import api
from flask_pydantic import validate
from controls.user import UserCtl
from common.web import AdvResource
from flask import request
from common.verify_token import require_token,get_request_user

@api.route('/')
class UserView(AdvResource):
    model = User
    control = UserCtl
    exclude_fields = ["password"]
    extend_fields = ['todos','tokens']

    @require_token
    def get(self):
        """查看单个用户"""
        args = request.args.to_dict()
        user = get_request_user()
        args['f_id'] = user.id
        return self.get_page(args)

    @api.expect(vm.UserCreateOrPutReq.rest_x_model(api))
    @validate()
    @require_token
    def post(self, body: vm.UserCreateOrPutReq):
        """创建用户"""
        user = self.control.create(body)
        ret = user.to_dict(exclude_fields=self.exclude_fields)
        # self.control.send_welcome_email(user)
        return ret

    @api.expect(vm.UserCreateOrPutReq.rest_x_model(api))
    @validate()
    @require_token
    def put(self, body: vm.UserCreateOrPutReq):
        """完整更新用户"""
        user = get_request_user()
        ctl = self.control.new_by_id(user.id)
        user = ctl.update(body)
        return user.to_dict(exclude_fields=self.exclude_fields)

    @api.expect(vm.UserPatchReq.rest_x_model(api))
    @validate()
    @require_token
    def patch(self, body: vm.UserPatchReq):
        """部分更新用户"""
        user = get_request_user()
        ctl = self.control.new_by_id(user.id)
        user = ctl.update(body)
        return user.to_dict(exclude_fields=self.exclude_fields)

    @require_token
    def delete(self):
        """删除用户"""
        user = get_request_user()
        ctl = self.control.new_by_id(user.id)
        return ctl.delete()
