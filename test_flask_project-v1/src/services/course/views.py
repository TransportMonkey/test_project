from common.verify_token import require_token,get_request_user
from model.course import Course
from flask_restx import Resource
from services.course import view_model as vm
from . import api
from flask_pydantic import validate
from controls.course import CourseCtl
from common.web import AdvResource
from flask import request


@api.route('/')
class CourseView(AdvResource):
    model = Course
    control = CourseCtl
    extend_fields = ["user_name"] # 扩展字段
    include_fields = None # 原有字段
    exclude_fields = ['user_id'] # 过滤字段

    @require_token
    def get(self):
        """查看课程列表"""
        args = request.args.to_dict()
        user = get_request_user()
        args['f_user_id'] = user.id
        return self.get_page(args)

    @api.expect(vm.CourseReq.rest_x_model(api))
    @validate()
    @require_token
    def post(self, body: vm.CourseReq):
        """选课"""
        user = get_request_user()
        self.control.select_courses(user, body)
        return 'ok'

@api.route('/<int:course_id>/')
class CoursesView(Resource):
    model = Course
    control = CourseCtl
    exclude_fields = ['user_id','id']

    def get(self,course_id):
        """查看选修课程的学生"""
        return self.control.show_all_student(course_id)

    @require_token
    def delete(self, course_id):
        """退课"""
        user = get_request_user()
        ctl = self.control.find_course(user.id,course_id)
        return ctl.delete()


@api.route('/create/')
class CreateView(Resource):
    model = Course
    control = CourseCtl

    @api.expect(vm.CourseReq.rest_x_model(api))
    @validate()
    def post(self, body: vm.CourseReq):
        """创建课程"""
        course = self.control.create(body)
        return course.to_dict()
