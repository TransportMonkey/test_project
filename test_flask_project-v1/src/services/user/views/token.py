from model.user import Token
from services.user import api
from controls.user import TokenCtl
from common.web import AdvResource
from flask import Response, json
from flask_pydantic import validate
from services.user import view_model as vm
from common.verify_token import require_token,get_user_token


@api.route('/token/')
class TokenView(AdvResource):
    model = Token
    control = TokenCtl

    @api.expect(vm.TokenReq.rest_x_model(api))
    @validate()
    def post(self, body:vm.TokenReq):
        """登录入口"""
        raw_token= self.control.create(body.user_name,body.password)
        response = Response(
            json.dumps({'token': raw_token}),
            status=200,
            mimetype='application/json')
        return response  # 直接返回 Response 对象

    @require_token
    def delete(self):
        """退出登录"""
        token = get_user_token()
        token.delete()
        return "ok"


