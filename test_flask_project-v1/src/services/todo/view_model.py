from common.view_model import RestXBaseModel
from pydantic import Field


class TodoReq(RestXBaseModel):
    name: str = Field(description="todo名称")
    done: bool = Field(description="是否完成")


class TodoPatchReq(RestXBaseModel):
    name: str = Field(None,description="todo名称")
    done: bool = Field(None,description="是否完成")
