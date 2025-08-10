from model.blog import Article,Category,Comment
from services.blog import view_model as vm
from .base_ctl import BaseCtl
from common import logmode


class ArticleCtl(BaseCtl):
    model_cls = Article

    @property
    def article(self) -> Article:
        return self.model

    @classmethod
    def release(cls, args: vm.ArticlePatchReq) -> Article:
        logmode.info("release article args %s", args)
        return cls.model_cls.create(**args.model_dump(exclude_none=True))

    def delete(self):
        # 删除_id
        for comment in self.article.comments:
            comment.delete()
        # 删除id
        self.article.delete()


class CategoryCtl(BaseCtl):
    model_cls = Category

    @property
    def category(self) -> Category:
        return self.model

    @classmethod
    def create(cls,args: vm.CategoryCreateOrPutReq) -> Category:
        return cls.model_cls.create(**args.model_dump(exclude_none=True))



class CommentCtl(BaseCtl):
    model_cls = Comment

    @property
    def comment(self) -> Comment:
        return self.model

    @classmethod
    def publish(cls, args: vm.CommentCreateOrPutReq) -> Comment:
        return cls.model_cls.create(**args.model_dump(exclude_none=True))


