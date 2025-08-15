from flask import request
from model.user import File
from services.user import api
from controls.user import FileCtl
from common.web import AdvResource
from common.verify_token import require_token,get_request_user

@api.route('/file/')
class FileView(AdvResource):
    model = File
    control = FileCtl
    exclude_fields = ['user_id']

    @require_token
    def get(self):
        """查看文件"""
        args = request.args.to_dict()
        user = get_request_user()
        args['f_user_id'] = user.id
        return self.get_page(args)

    @require_token
    def post(self):
        """上传文件"""
        user = get_request_user()
        file = self.control.upload(user.id)
        return file.to_dict(exclude_fields=self.exclude_fields)



