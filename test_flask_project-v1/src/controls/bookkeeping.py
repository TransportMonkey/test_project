from datetime import datetime
from werkzeug.exceptions import BadRequest
from model.bookkeeping import Record,Expense
from .base_ctl import BaseCtl
import typing
from services.bookkeeping import view_model as vm
from common import logmode

class ExpenseCtl(BaseCtl):
    model_cls = Expense

    @property
    def expense(self) -> Expense:
        return self.model

    @classmethod
    def exist_expense_name(cls, name: str, user_id) -> bool:
        return cls.model_cls.where(name=name, user_id=user_id).first() is not None

    @classmethod
    def create(cls, user_id, args: vm.ExpenseReq) -> Expense:
        return cls.model_cls.create(user_id=user_id,**args.model_dump(exclude_none=True))

    def update(self, args: typing.Union[vm.ExpensePatchReq,vm.ExpenseReq]):
        """更新Expense"""
        args = args.model_dump(exclude_none=True)
        if len(args) > 0:
            if "name" in args and args["name"] != self.expense.name:
                if self.exist_expense_name(args["name"],self.expense.user_id):
                    raise BadRequest("expense名称已创建，请更换名称再重试")
            logmode.info("update expense[%s-%s] args %s", self.expense.id, self.expense.name, args)
            self.expense.update(**args)
        return self.expense

    def delete(self):
        for record in self.expense.records:
            record.delete()
        self.expense.delete()

class RecordCtl(BaseCtl):
    model_cls = Record

    @property
    def record(self) -> Record:
        return self.model

    @classmethod
    def create_record(cls, user_id, args: vm.RecordReq) -> Record:
        expense = Expense.where(id=args.expense_id).first()
        if not expense:
            raise BadRequest('收支分类不存在')
        print(args.income,args.spend)
        record_data = (args.income,args.spend,expense.id)
        result = cls.insert_data(record_data)
        return cls.model_cls.create(user_id=user_id,**result)

    @classmethod
    def insert_data(cls, record_data) -> dict:
        result = {
                    'income':record_data[0],
                    'spend': record_data[1],
                    'record_time': datetime.now(),
                    'expense_id': record_data[2],
                 }
        return result

    def update(self, args: typing.Union[vm.RecordPatchReq,vm.RecordReq]):
        """更新收支记录"""
        args = args.model_dump(exclude_none=True)
        if len(args) > 0:
            expense = Expense.where(id=args['expense_id']).first()
            if not expense:
                raise BadRequest('更新失败，收支分类不存在')
            self.record.update(**args)
        return self.record

    @classmethod
    def calc_income_spend(cls, user_id, start_time, end_time):
        # 使用 ORM 查询符合条件的记录，并对 income 和 spend 进行统计
        query = cls.model_cls.query.filter(
            cls.model_cls.user_id == user_id,
            cls.model_cls.record_time >= start_time,
            cls.model_cls.record_time <= end_time,
            # cls.model_cls.user_id.in_([user_id]),
            # cls.model_cls.user_id.notin_([user_id]),

        )
        records = query.all()
        total_income, total_spend = 0,0
        for record in records:
            total_income += record.income
            total_spend += record.spend
        # # 统计 income 和 spend 的总和，将 NULL 替换为 0，并确保结果不为 None
        # result = query.with_entities(
        #     func.coalesce(func.sum(cls.model_cls.income), 0),
        #     func.coalesce(func.sum(cls.model_cls.spend), 0)
        # ).first()
        #
        # # 解包结果，确保返回的是两个数值
        # total_income, total_spend = result if result else (0, 0)
        return total_income, total_spend

    @classmethod
    def count_record(cls, user_id, args: vm.CountPatchReq):
        start_time = datetime.strptime(args.start_time, '%Y-%m-%d')
        end_time = datetime.strptime(args.end_time, '%Y-%m-%d')
        end_time = end_time.replace(hour=23, minute=59, second=59)
        return cls.calc_income_spend(user_id, start_time, end_time)

    @classmethod
    def handle_date_format(cls, start_time, end_time)->str:
        # 将字符串转换为 datetime 对象
        new_start_time = datetime.strptime(start_time, '%Y-%m-%d')
        new_end_time = datetime.strptime(end_time, '%Y-%m-%d')
        # 判断是否同一年
        if new_start_time.year == new_end_time.year:
            # 如果是同一年，按照指定格式输出
            result = f"{new_start_time.year}.{new_start_time.strftime('%m.%d')}~{new_end_time.strftime('%m.%d')}"
            return result
        return f'{start_time}~{end_time}'





