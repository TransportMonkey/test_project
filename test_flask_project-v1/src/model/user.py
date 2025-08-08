from common.db import BaseModel, db


class User(BaseModel):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, nullable=False, comment="用户名")
    age = db.Column(db.Integer, comment="年龄", nullable=False)
    gender = db.Column(db.Integer, nullable=False, comment="性别 1:男,2:女")
    email = db.Column(db.String(80), index=True, nullable=False, comment="邮箱")
    password = db.Column(db.String(80), index=True, nullable=False, comment="密码")
    todos = db.relationship(
        'Todo',
        primaryjoin='Todo.id==foreign(model.user.User.id)',
        uselist=True
    )