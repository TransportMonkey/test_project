import os
from flask import send_file
from werkzeug.exceptions import Forbidden
from model.user import File
from services.user import api
from werkzeug.exceptions import NotFound
from controls.user import FileCtl
from common.web import AdvResource
from common.util import get_config
from common.verify_token import require_token,get_request_user

@api.route('/download/<int:file_id>/')
class DownloadView(AdvResource):
    model = File
    control = FileCtl
    exclude_fields = ['id' ,'user_id']

    @require_token
    def get(self, file_id):
        """下载文件"""
        ctl = self.control.new_by_id(file_id)
        user = get_request_user()
        if ctl.file.user_id != user.id:
            raise Forbidden('不允许下载他人文件他人的文件')
        user_dir = os.path.join(get_config('SOURCE_ROOT'),str(ctl.file.user_id))
        down_file_path = os.path.join(user_dir,ctl.file.name)
        if not os.path.isfile(down_file_path):
            raise NotFound('未找到资源')
        return send_file(down_file_path,as_attachment=True)