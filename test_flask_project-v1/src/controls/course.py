from model.course import Course,StudentCourse
from services.course import view_model as vm
from .base_ctl import BaseCtl
from werkzeug.exceptions import BadRequest


class CourseCtl(BaseCtl):
    model_cls = Course

    @property
    def course(self) -> Course:
        return self.model

    @classmethod
    def create(cls, args: vm.CourseReq) -> Course:
        return cls.model_cls.create(**args.model_dump(exclude_none=True))

    @classmethod
    def select_courses(cls, user, args: vm.CourseReq):
        # 查询课程
        course = Course.where(name=args.name).first()
        # 检查课程是否存在
        if course:
            # 判断学生是否已选修课程
            if course in user.courses:
                raise BadRequest("您已选修了该课程，无需再次选修！")
            return StudentCourse.create(user_id=user.id, course_id=course.id)
        raise BadRequest("学生或课程不存在！")

    @classmethod
    def find_course(cls, user_id, course_id):
        stu_cor = StudentCourse.query.filter_by(user_id=user_id,course_id=course_id).first()
        if not stu_cor:
            raise BadRequest("课程不存在！")
        return stu_cor

    @classmethod
    def show_all_student(cls, course_id):
        course = cls.model_cls.query.filter_by(id=course_id).first()
        if course:
            all_students = [student.name for student in course.students]
            if len(all_students) > 0:
                return all_students
            raise BadRequest('未有学生选修该课程！')
        raise BadRequest('课程不存在！')


