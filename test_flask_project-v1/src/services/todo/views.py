from model.todo import Todo
from flask_restx import Resource
from services.todo import view_model as vm
from . import api
from flask_pydantic import validate
from controls.todo import TodoCtl


@api.route('/')
class TodosView(Resource):
    model = Todo
    control = TodoCtl
    extend_fields = ["user_name"] # 扩展字段
    include_fields = None # 原有字段

    exclude_fields = ["user_id"] # 过滤字段

    def get(self):
        """查看todo列表"""
        resp = []
        todos: list = self.model.all()
        for todo in todos:
            resp.append(todo.to_dict(exclude_fields=self.exclude_fields,extend_fields=self.extend_fields,include_fields=self.include_fields))
        return resp

    @api.expect(vm.TodoCreateOrPutReq.rest_x_model(api))
    @validate()
    def post(self, body: vm.TodoCreateOrPutReq):
        """创建Todo"""
        todo = self.control.create(body)
        return todo.to_dict(exclude_fields=self.exclude_fields)


@api.route('/<int:todo_id>/')
class TodoView(Resource):
    model = Todo
    control = TodoCtl
    exclude_fields = ['user_id','id']

    def get(self, todo_id):
        """查看单个todo"""
        todo = self.model.find_or_fail(todo_id)

        return todo.to_dict(exclude_fields=self.exclude_fields)

    @api.expect(vm.TodoCreateOrPutReq.rest_x_model(api))
    @validate()
    def put(self, todo_id, body: vm.TodoCreateOrPutReq):
        """完整更新todo"""
        ctl = self.control.new_by_id(todo_id)
        todo = ctl.update(body)
        return todo.to_dict(exclude_fields=self.exclude_fields)

    @api.expect(vm.TodoPatchReq.rest_x_model(api))
    @validate()
    def patch(self, todo_id, body: vm.TodoPatchReq):
        """部分更新todo"""
        ctl = self.control.new_by_id(todo_id)
        todo = ctl.update(body)
        return todo.to_dict(exclude_fields=self.exclude_fields)

    def delete(self, todo_id):
        """删除todo"""
        ctl = self.control.new_by_id(todo_id)
        return ctl.simple_delete()