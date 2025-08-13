import typing
from model.todo import Todo
from services.todo import view_model as vm
from .base_ctl import BaseCtl
from common import logmode
from werkzeug.exceptions import BadRequest


class TodoCtl(BaseCtl):
    model_cls = Todo

    @property
    def todo(self) -> Todo:
        return self.model

    @classmethod
    def exist_todo_name(cls, name: str,user_id)-> bool:
        """
        select * from todo where name = '做作业' and user_id == 2;
        """
        return cls.model_cls.where(name=name,user_id=user_id).first() is not None
        # if todo is not None:
        #     return True
        # return False
        # return any([self.todo.user_id == todo.user_id for todo in todo_list])
        # return all([self.todo.user_id != todo.user_id for todo in todo_list])
        # for todo in todo_list:
        #     if self.todo.user_id == todo.user_id:
        #         return True
        # return False

    @classmethod
    def create(cls, args: vm.TodoPatchReq) -> Todo:
        logmode.info("create todo args %s", args)
        if cls.exist_todo_name(args.name,args.user_id):
            raise BadRequest("todo名称已创建，请更换名称再重试")
        return cls.model_cls.create(**args.model_dump(exclude_none=True))

    def update(self, args: typing.Union[vm.TodoPatchReq,vm.TodoReq]):
        """更新todo"""
        args = args.model_dump(exclude_none=True)
        if len(args) > 0:
            if "name" in args and args["name"] != self.todo.name:
                if self.exist_todo_name(args["name"],self.todo.user_id):
                    raise BadRequest("todo名称已创建，请更换名称再重试")
            logmode.info("update todo[%s-%s] args %s", self.todo.id, self.todo.name, args)
            self.todo.update(**args)
        return self.todo