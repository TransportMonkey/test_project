from model.blog import Article
from services.blog import view_model as vm
from services.blog import api
from flask_pydantic import validate
from common.web import AdvResource
from flask import request
from controls.blog import  ArticleCtl
from common.verify_token import require_token,get_request_user
from werkzeug.exceptions import Forbidden


@api.route('/article/')
class ArticleView(AdvResource):
    model = Article
    control = ArticleCtl
    exclude_fields = ['user_id']  # 过滤字段

    @require_token
    def get(self):
        """查看文章列表"""
        args = request.args.to_dict()
        user = get_request_user()
        args['f_user_id'] = user.id
        return self.get_page(args)

    @api.expect(vm.ArticleCreateOrPutReq.rest_x_model(api))
    @validate()
    @require_token
    def post(self, body: vm.ArticlePatchReq):
        """发布文章"""
        user = get_request_user()
        body.user_id = user.id
        todo = self.control.release(body)
        return todo.to_dict(exclude_fields=self.exclude_fields)



@api.route('/article/<int:article_id>/')
class ArticlesView(AdvResource):
    model = Article
    control = ArticleCtl
    extend_fields = ['comments','test'] # 扩展字段(指定模型的属性)

    @require_token
    def get(self, article_id):
        """查看文章"""
        article = self.model.find_or_fail(article_id)
        user = get_request_user()
        if article.user_id != user.id:
            raise Forbidden('文章不存在')
        return article.to_dict(exclude_fields=self.extend_fields)


    @require_token
    def delete(self, article_id):
        """删除文章"""
        ctl = self.control.new_by_id(article_id)
        user = get_request_user()
        if ctl.article.user_id != user.id:
            raise Forbidden('文章不存在')
        ctl.delete()
        return