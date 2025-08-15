
from model.blog import Category
from common.verify_token import require_token, get_request_user
from services.blog import view_model as vm
from services.blog import api
from flask_pydantic import validate
from common.web import AdvResource
from flask import request
from controls.blog import CategoryCtl



@api.route('/category/')
class CategoryView(AdvResource):
    model = Category
    control = CategoryCtl

    @require_token
    def get(self):
        """查看分类"""
        args = request.args.to_dict()
        user = get_request_user()
        args['f_user_id'] = user.id
        return self.get_page(args)

    @api.expect(vm.CategoryCreateOrPutReq.rest_x_model(api))
    @validate() # 校验参数
    @require_token
    def post(self, body: vm.CategoryCreateOrPutReq):
        """创建分类"""
        user = get_request_user()
        category = self.control.create(user.id,body)
        return category.to_dict()


@api.route('/category/<int:category_id>/')
class CategoriesView(AdvResource):
    model = Category
    control = CategoryCtl
    extend_fields = ['title']
    exclude_fields = ['id']

    @require_token
    def get(self, category_id):
        """查看单个分类"""
        category = self.model.find_or_fail(category_id)
        return category.to_dict(exclude_fields=self.exclude_fields,extend_fields=self.extend_fields)
