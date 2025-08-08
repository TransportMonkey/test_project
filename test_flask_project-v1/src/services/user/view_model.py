from common.view_model import RestXBaseModel
from pydantic import Field


class UserCreateOrPutReq(RestXBaseModel):
    name: str = Field(description="用户名")
    age: int = Field(description="年龄", ge=1, le=150)
    gender: int = Field(description="性别", ge=1, le=2)
    email: str = Field(description="邮箱", max_length=80)
    password: str = Field(description="密码", max_length=80)


class UserPatchReq(RestXBaseModel):
    name: str = Field(None, description="用户名")
    age: int = Field(None, description="年龄", ge=1, le=150)
    gender: int = Field(None, description="性别", ge=1, le=2)
    email: str = Field(None, description="邮箱", max_length=80)
    password: str = Field(None, description="密码", max_length=80)
