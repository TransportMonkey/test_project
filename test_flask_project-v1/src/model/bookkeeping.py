from common.db import BaseModel, db

"""
定义Expense和Record类，都继承BaseModel基类
1、Expense表的结构：
            id(Integer)、name(String)、user_id(Integer)
2、Record表的结构：
            id(Integer)、income(Float)、
            spend(Float)、Expense_id(Integer)、
            user_id(Integer)、record_time(DateTime)
3、表的关联关系：
        user与Expense是一对多关系(一个用户有多个收支分类)
        Expense与Record是一对多关系(一个收支分类有多条记账记录)
4、通过relationship建立表与表的关联，访问关联的数据
"""

class Expense(BaseModel):
    __tablename__ = 'expense'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True,unique=True, nullable=False,comment='收支分类名称')
    user_id = db.Column(db.Integer,index=True,nullable=False,comment='用户ID')
    records = db.relationship(
        'Record', # 指定关联模型
        primaryjoin='Expense.id == foreign(Record.expense_id)', # 指定关联条件
        uselist=True # 指定关联类型
    )

class Record(BaseModel):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    income = db.Column(db.Float, index=True,comment='收入',nullable=False)
    spend = db.Column(db.Float, index=True,comment='支出',nullable=False)
    record_time = db.Column(db.DateTime,index=True,nullable=False,comment='记录时间')
    expense_id = db.Column(db.Integer,index=True,nullable=False,comment='收支分类ID')
    user_id = db.Column(db.Integer, index=True,nullable=False, comment='用户ID')
    expense = db.relationship(
        'Expense',  # 指定关联模型
        primaryjoin='Expense.id == foreign(Record.expense_id)',  # 指定关联条件
        uselist=False  # 指定关联类型
    )
    user = db.relationship(
        'User',  # 指定关联模型
        primaryjoin='model.user.User.id == foreign(Record.user_id)',  # 指定关联条件
        uselist=False  # 指定关联类型
    )