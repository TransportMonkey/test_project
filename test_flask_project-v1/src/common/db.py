from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.collections import InstrumentedList
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
            if isinstance(v, datetime):
                v = v.isoformat()
            rest[column] = v

        if extend_fields is not None:
            for field in extend_fields:
                if hasattr(self, field):
                    v = getattr(self, field)
                    if isinstance(v,InstrumentedList):
                        rest[field] = [vv.to_dict() for vv in v]
                    # if isinstance(v,list):
                    #     tmp_v = []
                    #     for vv in v:
                    #         if hasattr(vv,"to_dict"):
                    #             tmp_v.append(vv.to_dict())
                    #         else:
                    #             tmp_v.append(vv)
                    #     rest[field] = tmp_v
                    elif hasattr(v, "to_dict"):
                        rest[field] = v.to_dict()
                    else:
                        rest[field] = v
        return rest



