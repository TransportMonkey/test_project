from model.blog import Comment
from services.blog import view_model as vm
from services.blog import api
from flask_pydantic import validate
from common.web import AdvResource
from flask import request
from controls.blog import  CommentCtl
from common.verify_token import require_token,get_request_user
from werkzeug.exceptions import Forbidden


@api.route('/comment/')
class CommentsView(AdvResource):
    model = Comment
    control = CommentCtl
    exclude_fields = []  # 过滤字段

    @require_token
    def get(self):
        """查看评论"""
        args = request.args.to_dict()
        # user = get_request_user()
        # args['f_user_id'] = user.id
        return self.get_page(args)

    @api.expect(vm.CommentCreateOrPutReq.rest_x_model(api))
    @validate()
    @require_token
    def post(self, body: vm.CommentCreateOrPutReq):
        """评论文章"""
        user = get_request_user()
        comment = self.control.publish(user.id,body)
        return comment.to_dict(exclude_fields=self.exclude_fields)


@api.route('/comment/<int:comment_id>/')
class CommentView(AdvResource):
    model = Comment
    control = CommentCtl

    @require_token
    def delete(self, comment_id: int):
        """删除评论"""
        ctl  = self.control.new_by_id(comment_id)
        user = get_request_user()
        if ctl.comment.user_id != user.id:
            raise Forbidden(description="不允许删除他人的评论")
        ctl.simple_delete()
        return




