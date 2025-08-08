import typing
from common import db


class BaseCtl:
    model_cls: typing.Type[db.BaseModel]
    model: db.BaseModel

    def __init__(self, model: db.BaseModel):
        self.model = model

    @classmethod
    def new_by_id(cls, _id: int) -> "BaseCtl":
        model = cls.model_cls.find_or_fail(_id)
        return cls(model)

    def simple_delete(self):
        self.model.delete()
        return "ok"

    def simple_update(self, **kwargs) -> db.BaseModel:
        return self.model.update(**kwargs)

    def simple_create(self, **kwargs) -> db.BaseModel:
        return self.model_cls.create(**kwargs)
