import typing
from flask_restx import Resource
from sqlalchemy import or_, and_, desc, asc


class PageResourceMixin:
    model: typing.Any
    ORDER_PRE = 'o_'
    FILTER_PRE = 'f_'
    SEARCH_PRE = 's_'

    page_number: int
    limit: int
    total: int
    query: typing.Any
    default_limit = 10
    select_fields = ()  # search field list

    def pre_page(self, params: dict):
        """预分页处理"""
        self.page_number = int(params.get("page", 1))
        self.limit = int(params.get("limit", self.default_limit))
        if self.limit <= 0:
            self.limit = self.default_limit

    def page(self):
        self.query = self.query.offset((self.page_number - 1) * self.limit).limit(self.limit)
        return self

    def filter(self, param):
        filters = {k[2:]: v for k, v in param.items() if k.startswith(self.FILTER_PRE)}
        for field, value in filters.items():
            if field in self.model.columns:
                self.query = self.query.filter_by(**{field: value})

    def search(self, params):
        """ 模糊查询  (url中 &=%26, |=%7C, "=%22)
        支持特定字段: s_name=a%26b
        """

        _fields_search = dict([(k[2:], v) for k, v in params.items() if k.startswith(self.SEARCH_PRE)])
        if not _fields_search:
            return self

        def _field_search(_fn, _v):
            """ 单个字段的查询
            :return subquery | None
            """

            _field = getattr(self.model, _fn, None)
            if not _field:
                return

            pattern = f'%{_v}%'
            return _field.like(pattern)

        for k, v in _fields_search.items():
            search_expr = _field_search(k, v)
            if search_expr is not None:
                self.query = self.query.filter(search_expr)

        return self

    def calc_total(self):
        self.total = self.query.count()
        return self


class AdvResource(PageResourceMixin, Resource):
    model: typing.Any

    list_fields = None  # get_list_data function use, for get object's fields
    exclude_fields = None  # get_list_data function use, for exclude object's fields
    extend_fields = None  # get_list_data function use, for extend object's fields
    include_fields = None

    def select(self, query, params):
        self.query = query
        # 过滤
        self.filter(params)

        # 模糊查询
        self.search(params)

        # todo 支持排序 o_{field}
        return self

    def get_list_data(self, model):
        return model.to_dict(
            include_fields=self.include_fields,
            exclude_fields=self.exclude_fields,
            extend_fields=self.extend_fields
        )

    def get_page(self, req, query=None):
        """获取分页数据
        :param req: flask.request or args
        :param query: query
        """
        args = req.args if hasattr(req, 'args') else req
        query = query if query is not None else self.model.query
        self.select(query, args).calc_total()
        self.pre_page(args)
        self.page()

        models = self.query.all()
        datas = [self.get_list_data(model) for model in models]

        page_kwargs = dict(
            total=self.total, limit=self.limit,
            page=self.page_number,
            count=len(datas)
        )
        return dict(data=datas, **page_kwargs)