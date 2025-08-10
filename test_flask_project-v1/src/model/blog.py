from common.db import BaseModel, db
from sqlalchemy.sql import func


"""
专栏（分类）
id：
name:

文章
id:
title:
content:
category_id #分类id
user_id:


评论
id:
content:
user_id:
article_id:
"""

# 定义文章专栏模型
class Category(BaseModel):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True) # 专栏ID
    name = db.Column(db.String(80), index=True,unique=True, nullable=False,comment='专栏名称') # 专栏名称


    articles = db.relationship(
        'Article',
        primaryjoin='Category.id==foreign(Article.category_id)',
        uselist=True
    )


# 定义个人文章模型
class Article(BaseModel):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True) # 文章ID
    title = db.Column(db.String(80),nullable=False,comment='文章标题') # 文章标题
    content = db.Column(db.Text, nullable=False, comment='文章内容')  # 文章内容
    status = db.Column(db.Boolean, index=True,comment="是否发布", default=True,server_default='1') # 文章发布状态
    visible = db.Column(db.Boolean, comment="文章可见范围", default=True,server_default='1') # 文章可见范围
    user_id = db.Column(db.Integer,index=True,comment="用户ID",nullable=False) # 外键，表示该文章所属的用户
    category_id = db.Column(db.Integer,index=True,comment="专栏ID",nullable=False) # 外键，表示该文章所属的专栏
    category = db.relationship(
        'Category',
        primaryjoin='Category.id==foreign(Article.category_id)',
        uselist=False
    )

    comments = db.relationship(
        'Comment',
        primaryjoin='Article.id==foreign(Comment.article_id)',
        uselist=True
    )
    @property
    def test(self):
        return [1,2,3]

# 定义评论模型
class Comment(BaseModel):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), comment='文章内容')  # 文章内容
    user_id = db.Column(db.Integer, nullable=False,comment='评论者姓名') # 评论者姓名
    created_at = db.Column(db.DateTime,default=func.now(),nullable=False,index=True) # 插入时自动设为当前时间
    article_id = db.Column(db.Integer,index=True,comment="被评论的文章ID",nullable=False) # 外键，表示该条评论所属的文章

    article = db.relationship(
        'Article',
        primaryjoin='Article.id==foreign(Comment.article_id)',
        uselist=False
    )