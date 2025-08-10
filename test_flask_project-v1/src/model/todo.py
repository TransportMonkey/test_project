from common.db import BaseModel, db


class Todo(BaseModel):
    __tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, nullable=False, comment="todo名称")
    done = db.Column(db.Boolean, index=True,comment="是否完成", default=False,server_default='0',nullable=False)
    user_id = db.Column(db.Integer,index=True,comment="用户ID",nullable=False)
    user = db.relationship(
        'User',
        primaryjoin='model.user.User.id==foreign(Todo.user_id)',
        uselist=False,
    )