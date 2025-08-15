from common.db import BaseModel, db

"""
定义Todo类，继承BaseModel基类
1、user表的结构：
    id(Integer)、name(String)、done(Boolean)、user_id(Integer)
2、表的关联关系：
        user与todo是多对一关系(一个todo对应一个用户)
3、通过relationship建立表与表的关联，访问关联的数据
"""

class Todo(BaseModel):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, nullable=False, comment="todo名称")
    done = db.Column(db.Boolean, index=True,comment="是否完成", default=False,server_default='0',nullable=False)
    user_id = db.Column(db.Integer,index=True,comment="用户ID",nullable=False)
    user = db.relationship(
        'User', # 指定关联模型
        primaryjoin='model.user.User.id==foreign(Todo.user_id)', # 指定连接条件
        uselist=False, # 指定关系类型
    )