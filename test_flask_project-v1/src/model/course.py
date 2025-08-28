from common.db import BaseModel, db

"""
定义Todo类，继承BaseModel基类
1、user表的结构：
    id(Integer)、name(String)、done(Boolean)、user_id(Integer)
2、表的关联关系：
        user与todo是多对一关系(一个todo对应一个用户)
3、通过relationship建立表与表的关联，访问关联的数据
"""

class StudentCourse(BaseModel):
    __tablename__ = 'student_course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    course_id = db.Column(db.Integer, nullable=False, index=True)

    # 正确的外键关系
    user = db.relationship(
        'User',
        primaryjoin='User.id == foreign(StudentCourse.user_id)',
        uselist=False,
        back_populates="enrollments"
    )
    course = db.relationship(
        'Course',
        primaryjoin='Course.id == foreign(StudentCourse.course_id)',  # ✅ 修正了这里
        uselist=False,
        back_populates="enrollments"
    )

    # 可选：添加外键约束（推荐）
    __table_args__ = (
        db.ForeignKeyConstraint(['user_id'], ['user.id']),
        db.ForeignKeyConstraint(['course_id'], ['course.id']),
        db.Index('idx_user_course', 'user_id', 'course_id', unique=True),  # 防止重复选课
    )


class Course(BaseModel):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False, comment="课程名称")

    # back_populates 到中间表
    enrollments = db.relationship("StudentCourse", back_populates="course")

    # 便捷访问：所有选修该课程的学生
    students = db.relationship(
        "User",
        secondary="student_course",
        primaryjoin="Course.id == StudentCourse.course_id",
        secondaryjoin="StudentCourse.user_id == User.id",
        viewonly=True,
        uselist=True,
        back_populates="courses"
    )