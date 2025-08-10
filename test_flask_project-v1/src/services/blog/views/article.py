from model.blog import Article
from services.blog import view_model as vm
from services.blog import api
from flask_pydantic import validate
from common.web import AdvResource
from flask import request
from controls.blog import  ArticleCtl


@api.route('/article/')
class ArticleView(AdvResource):
    model = Article
    control = ArticleCtl
    exclude_fields = ['user_id']  # 过滤字段

    def get(self):
        """查看文章列表"""
        return self.get_page(request)

    @api.expect(vm.ArticleCreateOrPutReq.rest_x_model(api))
    @validate()
    def post(self, body: vm.ArticleCreateOrPutReq):
        """发布文章"""
        todo = self.control.release(body)
        return todo.to_dict(exclude_fields=self.exclude_fields)



@api.route('/article/<int:article_id>/')
class ArticlesView(AdvResource):
    model = Article
    control = ArticleCtl
    extend_fields = ['comments','test'] # 扩展字段(指定模型的属性)

    def get(self, article_id):
        """查看文章"""
        article = self.model.find_or_fail(article_id)
        return article.to_dict(extend_fields=self.extend_fields)

    def delete(self, article_id):
        """删除文章"""
        ctl = self.control.new_by_id(article_id)
        ctl.delete()
        return