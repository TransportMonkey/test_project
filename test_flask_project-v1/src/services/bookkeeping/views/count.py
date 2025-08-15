from model.bookkeeping import Record
from services.bookkeeping import view_model as vm
from services.bookkeeping import api
from flask_pydantic import validate
from common.web import AdvResource
from controls.bookkeeping import RecordCtl
from common.verify_token import require_token,get_request_user

@api.route('/count/')
class CountView(AdvResource):
    model = Record
    control = RecordCtl

    @api.expect(vm.CountReq.rest_x_model(api))
    @validate()
    @require_token
    def post(self, body: vm.CountPatchReq):
        """统计收支记录"""
        user = get_request_user()
        total_income, total_spend  = self.control.count_record(user.id,body)
        scope = self.control.handle_date_format(body.start_time, body.end_time)
        result = {
            'query_scope': scope,
            'total_income': f'{total_income:.2f} ￥',
            'total_spend': f'{total_spend:.2f} ￥'
        }
        return result


