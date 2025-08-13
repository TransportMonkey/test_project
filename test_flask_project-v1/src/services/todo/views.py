from common.verify_token import require_token,get_request_user,get_user_token
from model.todo import Todo
from flask_restx import Resource
from services.todo import view_model as vm
from . import api
from flask_pydantic import validate
from controls.todo import TodoCtl
from common.web import AdvResource
from flask import request
from werkzeug.exceptions import Forbidden


@api.route('/')
class TodosView(AdvResource):
    model = Todo
    control = TodoCtl
    extend_fields = ["user_name"] # 扩展字段
    include_fields = None # 原有字段
    exclude_fields = ['user_id','id'] # 过滤字段

    @require_token
    def get(self):
        """查看todo列表"""
        args = request.args.to_dict()
        user = get_request_user()
        args['f_user_id'] = user.id
        return self.get_page(args)

    @api.expect(vm.TodoReq.rest_x_model(api))
    @validate()
    @require_token
    def post(self, body: vm.TodoPatchReq):
        """创建Todo"""
        user = get_request_user()
        body.user_id = user.id
        todo = self.control.create(body)
        return todo.to_dict(exclude_fields=self.exclude_fields)



@api.route('/<int:todo_id>/')
class TodoView(Resource):
    model = Todo
    control = TodoCtl
    exclude_fields = ['user_id','id']

    @api.expect(vm.TodoReq.rest_x_model(api))
    @validate()
    @require_token
    def put(self, todo_id, body: vm.TodoReq):
        """完整更新todo"""
        ctl = self.control.new_by_id(todo_id)
        user = get_request_user()
        if ctl.todo.user_id != user.id:
            raise Forbidden('不允许更改他人的todo')
        todo = ctl.update(body)
        return todo.to_dict(exclude_fields=self.exclude_fields)

    @api.expect(vm.TodoPatchReq.rest_x_model(api))
    @validate()
    @require_token
    def patch(self,todo_id, body: vm.TodoPatchReq):
        """部分更新todo"""
        ctl = self.control.new_by_id(todo_id)
        user = get_request_user()
        if ctl.todo.user_id != user.id:
            raise Forbidden('不允许更改他人的todo')
        todo = ctl.update(body)
        return todo.to_dict(exclude_fields=self.exclude_fields)

    @require_token
    def delete(self, todo_id):
        """删除todo"""
        ctl = self.control.new_by_id(todo_id)
        user = get_request_user()
        if ctl.todo.user_id != user.id:
            raise Forbidden('不允许删除他人的todo')
        return ctl.simple_delete()