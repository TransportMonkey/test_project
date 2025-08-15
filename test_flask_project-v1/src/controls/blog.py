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
    def release(cls, user_id, args: vm.ArticleCreateOrPutReq) -> Article:
        logmode.info("release article args %s", args)
        return cls.model_cls.create(user_id=user_id,**args.model_dump(exclude_none=True))

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
    def create(cls, user_id, args: vm.CategoryCreateOrPutReq) -> Category:
        return cls.model_cls.create(user_id=user_id,**args.model_dump(exclude_none=True))



class CommentCtl(BaseCtl):
    model_cls = Comment

    @property
    def comment(self) -> Comment:
        return self.model

    @classmethod
    def publish(cls, user_id, args: vm.CommentCreateOrPutReq) -> Comment:
        return cls.model_cls.create(user_id=user_id,**args.model_dump(exclude_none=True))


