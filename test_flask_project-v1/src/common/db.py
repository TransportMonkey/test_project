from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy_mixins import AllFeaturesMixin

Base = declarative_base()
# db: typing.Union[SQLAlchemy, sqlalchemy, sqlalchemy.orm]
db: SQLAlchemy


class BaseModel(Base, AllFeaturesMixin):
    __abstract__ = True

    def to_dict(self,exclude_fields=None,extend_fields=None,include_fields=None):

        rest = {}
        columns = self.columns
        if exclude_fields is not None:
            columns = filter(lambda x: x not in exclude_fields, columns)
        if include_fields is not None:
            columns = filter(lambda x: x in include_fields, columns)
        for column in columns:
            v = getattr(self, column)
            rest[column] = v

        if extend_fields is not None:
            for field in extend_fields:
                if hasattr(self, field):
                    v = getattr(self, field)
                    if hasattr(v, "to_dict"):
                        rest[field] = v.to_dict()
                    else:
                        rest[field] = v
        return rest



