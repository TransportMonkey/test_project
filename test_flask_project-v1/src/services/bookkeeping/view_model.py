from common.view_model import RestXBaseModel
from pydantic import Field

class ExpenseReq(RestXBaseModel):
    name: str = Field(description="收支分类名称")

class ExpensePatchReq(RestXBaseModel):
    name: str = Field(None,description="收支分类名称")

class RecordReq(RestXBaseModel):
    income: float = Field(0.0,description="收入")
    spend: float = Field(0.0,description="支出")
    expense_id: int = Field(description="收支分类ID")

class RecordPatchReq(RestXBaseModel):
    income: float = Field(0.0, description="收入")
    spend: float = Field(0.0, description="支出")
    expense_id: int = Field(None, description="收支分类ID")

class CountReq(RestXBaseModel):
    start_time: str = Field(description="开始时间")
    end_time: str = Field(description="结束时间")

class CountPatchReq(RestXBaseModel):
    start_time: str = Field(None,description="开始时间")
    end_time: str = Field(None,description="结束时间")