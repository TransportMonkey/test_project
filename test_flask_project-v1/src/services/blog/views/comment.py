from model.blog import Comment
from services.blog import view_model as vm
from services.blog import api
from flask_pydantic import validate
from common.web import AdvResource
from flask import request
from controls.blog import  CommentCtl


@api.route('/comment/')
class CommentsView(AdvResource):
    model = Comment
    control = CommentCtl
    exclude_fields = []  # 过滤字段

    def get(self):
        """查看评论"""
        # return self.model.all()
        return self.get_page(request)

    @api.expect(vm.CommentCreateOrPutReq.rest_x_model(api))
    @validate()
    def post(self, body: vm.CommentCreateOrPutReq):
        """评论文章"""
        todo = self.control.publish(body)
        return todo.to_dict(exclude_fields=self.exclude_fields)


@api.route('/comment/<int:comment_id>/')
class CommentView(AdvResource):
    model = Comment
    control = CommentCtl

    def delete(self, comment_id: int):
        """删除评论"""
        ctl  = self.control.new_by_id(comment_id)
        ctl.simple_delete()
        return




