from common.view_model import RestXBaseModel
from pydantic import Field


class CourseReq(RestXBaseModel):
    name: str = Field(description="课程名称")


class CoursePatchReq(RestXBaseModel):
    name: str = Field(None,description="课程名称")