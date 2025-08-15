from model.bookkeeping import Record
from services.bookkeeping import view_model as vm
from services.bookkeeping import api
from flask_pydantic import validate
from common.web import AdvResource
from flask import request
from controls.bookkeeping import RecordCtl
from common.verify_token import require_token,get_request_user
from werkzeug.exceptions import Forbidden, BadRequest


@api.route('/record/')
class RecordView(AdvResource):
    model = Record
    control = RecordCtl
    exclude_fields = ['user_id','record_time']

    @require_token
    def get(self):
        """查看收支列表"""
        args = request.args.to_dict()
        user = get_request_user()
        args['f_user_id'] = user.id
        return self.get_page(args)

    @api.expect(vm.RecordReq.rest_x_model(api))
    @validate()
    @require_token
    def post(self, body: vm.RecordReq):
        """新增收支记录"""
        # if body.income is None and body.expense is None:
        #     raise BadRequest("至少输入收入或支出")
        user = get_request_user()
        record = self.control.create_record(user.id,body)
        return record.to_dict(exclude_fields=self.exclude_fields)

@api.route('/record/<int:record_id>/')
class RecordsView(AdvResource):
    model = Record
    control = RecordCtl
    exclude_fields = ['user_id']

    @api.expect(vm.RecordReq.rest_x_model(api))
    @validate()
    @require_token
    def put(self, record_id, body: vm.RecordReq):
        """完整更新收支记录"""
        ctl = self.control.new_by_id(record_id)
        user = get_request_user()
        if ctl.record.user_id != user.id:
            raise Forbidden('不允许更改他人的收支记录')
        record = ctl.update(body)
        return record.to_dict(exclude_fields=self.exclude_fields)

    @api.expect(vm.RecordPatchReq.rest_x_model(api))
    @validate()
    @require_token
    def patch(self, record_id, body: vm.RecordPatchReq):
        """部分更新收支记录"""
        ctl = self.control.new_by_id(record_id)
        user = get_request_user()
        if ctl.record.user_id != user.id:
            raise Forbidden('不允许更改他人的收支记录')
        record = ctl.update(body)
        return record.to_dict(exclude_fields=self.exclude_fields)

    @require_token
    def delete(self, record_id):
        """删除收支记录"""
        ctl = self.control.new_by_id(record_id)
        user = get_request_user()
        if ctl.record.user_id != user.id:
            raise Forbidden('不允许删除他人的收支记录')
        return ctl.simple_delete()





