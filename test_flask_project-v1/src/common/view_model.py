from pydantic import BaseModel
from flask_restx import fields


class RestXBaseModel(BaseModel):
    __rest_x_model__ = None

    __field_type_map__ = {
        str: fields.String,
        int: fields.Integer,
        bool: fields.Boolean,

    }

    @classmethod
    def rest_x_model(cls, api):
        if cls.__rest_x_model__ is not None:
            return cls.__rest_x_model__
        model_fields = {}
        for field_name, field_info in cls.model_fields.items():
            field_type = field_info.annotation
            required = field_info.is_required()
            # 类型映射
            flask_field = cls.__field_type_map__.get(field_type, fields.Raw)

            # 设置默认值
            if not required and hasattr(field_info, "default"):
                flask_field.default = field_info.default

            model_fields[field_name] = flask_field

        return api.model(f"{cls.__name__}Model", model_fields)
