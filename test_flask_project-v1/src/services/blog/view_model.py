from common.view_model import RestXBaseModel
from pydantic import Field


class CategoryCreateOrPutReq(RestXBaseModel):
    name: str = Field('lift',description="专栏名称",max_length=80)

class CategoryPatchReq(RestXBaseModel):
    name: str = Field(None,description="专栏名称")

class ArticleCreateOrPutReq(RestXBaseModel):
    title: str = Field(description="文章标题")
    content: str = Field(description="文章内容")
    status: bool = Field(description="是否发布")
    visible: bool = Field(description="文章可见范围")
    user_id: int = Field(description="用户ID")
    category_id: int = Field(description="专栏ID")

class ArticlePatchReq(RestXBaseModel):
    title: str = Field(None,description="文章标题")
    content: str = Field(None,description="文章内容")
    status: bool = Field(None,description="是否发布")
    visible: bool = Field(None,description="文章可见范围")
    user_id: int = Field(None,description="用户ID")
    category_id: int = Field(None,description="专栏ID")

class CommentCreateOrPutReq(RestXBaseModel):
    content: str = Field(description="评论内容")
    user_id: int = Field(description="用户ID")
    article_id: int = Field(description="被评论的文章ID")

class CommentPatchReq(RestXBaseModel):
    content: str = Field(None, description="评论内容")
    user_id: int = Field(None, description="用户ID")
    article_id: int = Field(None, description="被评论的文章ID")