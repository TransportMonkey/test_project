from model.bookkeeping import Expense
from services.bookkeeping import view_model as vm
from services.bookkeeping import api
from flask_pydantic import validate
from common.web import AdvResource
from flask import request
from controls.bookkeeping import ExpenseCtl
from common.verify_token import require_token,get_request_user
from werkzeug.exceptions import Forbidden

@api.route('/expense/')
class ExpenseView(AdvResource):
    model = Expense
    control = ExpenseCtl
    exclude_fields = ['user_id']

    @require_token
    def get(self):
        """查看收支出分类"""
        args = request.args.to_dict()
        user = get_request_user()
        args['f_user_id'] = user.id
        return self.get_page(args)

    @api.expect(vm.ExpenseReq.rest_x_model(api))
    @validate()  # 校验参数
    @require_token
    def post(self, body: vm.ExpenseReq):
        """创建收支分类"""
        user = get_request_user()
        expense = self.control.create(user.id,body)
        return expense.to_dict(exclude_fields=self.exclude_fields)

@api.route('/expense/<int:expense_id>/')
class ExpensesView(AdvResource):
    model = Expense
    control = ExpenseCtl
    exclude_fields = ['user_id']

    @api.expect(vm.ExpensePatchReq.rest_x_model(api))
    @validate()
    @require_token
    def patch(self, expense_id, body: vm.ExpensePatchReq):
        """修改收支分类名称"""
        ctl = self.control.new_by_id(expense_id)
        user = get_request_user()
        if ctl.expense.user_id != user.id:
            raise Forbidden('不允许修改他人的收支分类名称')
        expense = ctl.update(body)
        return expense.to_dict(exclude_fields=self.exclude_fields)

    @require_token
    def delete(self, expense_id):
        """删除收支分类"""
        ctl = self.control.new_by_id(expense_id)
        user = get_request_user()
        if ctl.expense.user_id != user.id:
            raise Forbidden('不允许删除他人的收支分类名称')
        return ctl.delete()
