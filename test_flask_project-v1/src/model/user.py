from common.db import BaseModel, db

"""
定义User和Token类，都继承BaseModel基类
1、user表的结构：id(Integer)、name(String)、gender(Integer)、age(Integer)、email(String)、password(String)
2、token表的结构：id(Integer)、token(String)、expire_time(DateTime)、user_id(Integer)
3、file表的结构: id(Integer)、name(String)、path(String)、user_id(Integer)
3、表的关联关系：
        user与token是一对多关系(一个用户有多个token)
        user与todo是一对多关系(一个用户有多个todo)
        user与file是一对多关系(一个用户有多个文件)
4、通过relationship建立表与表的关联，访问关联的数据
"""

class User(BaseModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, nullable=False, comment="用户名")
    age = db.Column(db.Integer, comment="年龄", nullable=False)
    gender = db.Column(db.Integer, nullable=False, comment="性别 1:男,2:女")
    email = db.Column(db.String(80), index=True,unique=True, nullable=False, comment="邮箱")
    password = db.Column(db.String(80), index=True, nullable=False, comment="密码")
    todos = db.relationship(
        'Todo',
        primaryjoin='model.user.User.id==foreign(Todo.user_id)',
        uselist=True,
        cascade="all, delete-orphan",
    )
    tokens = db.relationship(
        'Token', # 指定关联的模型
        primaryjoin='User.id == foreign(Token.user_id)', # 指定连接条件
        uselist=True, # 指定关系类型
        cascade="all, delete-orphan",
    )
    categories = db.relationship(
        'Expense',  # 指定关联模型
        primaryjoin='model.user.User.id == foreign(Expense.user_id)',  # 指定关联条件
        uselist=True, # 指定关联类型
        cascade = "all, delete-orphan",
    )
    files = db.relationship(
        'File',  # 指定关联的模型
        primaryjoin='User.id == foreign(File.user_id)',  # 指定连接条件
        uselist=True,  # 指定关系类型
        cascade="all, delete-orphan",
    )
    # back_populates 到中间表
    enrollments = db.relationship("StudentCourse", back_populates="user")
    # 便捷访问：用户选修的所有课程
    courses = db.relationship(
        "Course",
        secondary="student_course",
        primaryjoin="User.id == StudentCourse.user_id",
        secondaryjoin="StudentCourse.course_id == Course.id",
        viewonly=True,
        uselist=True,
        back_populates="students"
    )

class Token(BaseModel):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(20),index=True, unique=True, nullable=False,comment='用户token')
    expire_time = db.Column(db.DateTime,nullable=False,comment='token过期时间')
    user_id = db.Column(db.Integer,nullable=False,comment='用户ID')
    user = db.relationship(
        'User', # 指定关联的模型
        primaryjoin='User.id == foreign(Token.user_id)', # 指定连接条件
        uselist=False, # 指定关系类型
    )

class File(BaseModel):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True, nullable=False, comment="文件名")
    user_id = db.Column(db.Integer,index=True, nullable=False, comment='用户ID')
    user = db.relationship(
        'User',  # 指定关联的模型
        primaryjoin='User.id == foreign(File.user_id)',  # 指定连接条件
        uselist=False,  # 指定关系类型
    )