from typing import Iterable, Optional

from flask_sqlalchemy import BaseQuery
from flask_restplus import Model

from backend.app.core.utils.logger import get_logger
from backend.app.core.models.mixins import JsonableMixin
from werkzeug.exceptions import abort
from http import HTTPStatus

logger = get_logger()


class QueryFilter:
    filter_methods: Iterable[callable]
    base_model: Model

    def __init__(self, filter_methods, base_model):
        self.filter_methods = filter_methods or []
        self.base_model = base_model

    def filter(self, query, args):
        for filter_method in self.filter_methods:
            try:
                query = filter_method(query, args)
            except KeyError:
                pass
        return query


def map_query_to_json(query):
    query = [obj.to_json() if isinstance(obj, JsonableMixin) else obj for obj in query]
    if not len(query):
        abort(HTTPStatus.NOT_FOUND, "Requested info is not found")
    return query


def paginate_query_to_list(query: BaseQuery, page: int, per_page: Optional[int]) -> list:
    if per_page:
        query = query.paginate(page, per_page).items
    query = map_query_to_json(query)
    return query


def find_param_by_atr(query, atr, value):
    result_query = query.filter(**{atr: value})
    if result_query.count() > 0 and value:
        return result_query
    return None
