import json
from http import HTTPStatus
from flask import request
import requests
from werkzeug.exceptions import abort

from app.core.utils.logger import get_logger
from app.core.utils.querying import QueryFilter

_MAPPER_TYPE_TO_METHOD = {
    "get": requests.get,
    "post": requests.post,
    "patch": requests.patch,
    "delete": requests.delete
}

logger = get_logger()


def paginate_external_api(items: list, paginate_options: dict) -> list:
    try:
        per_page = paginate_options.get("per_page")
        page_no = paginate_options.get("page")
        if not per_page:
            return items
        paginated_items = [items[i:i + per_page] for i in range(0, len(items), per_page)]
        return paginated_items[page_no - 1]
    except IndexError:
        abort(HTTPStatus.NOT_FOUND, "Items were not found")


def filter_external_api_items(filter_obj: QueryFilter,
                              items: list, filter_options: dict) -> list:
    filter_options = {k: v for k, v in filter_options.items() if v is not None}
    filtered_orders = filter_obj.filter(items, filter_options)
    return list(filtered_orders)


def map_type_to_method(http_type: str):
    return _MAPPER_TYPE_TO_METHOD[http_type.lower()]


def abort_if_not_ok_status(uri: str, method: str, abort_status_code: int = None, **kwargs) \
        -> requests.Response:
    """
    Function to abort request if request to external
    uri was not successful or if there were any
    connection errors (then returns 503 Service Unavailable)
    :param uri: external API URI
    :type uri: str
    :param method: HTTP method to send (GET, POST etc)
    :type method: str
    :param abort_status_code: abort status code, if not specified
                              response status code returned
    :type abort_status_code: int
    :param kwargs: parameters to request (headers, params, body etc)
    :type kwargs: dict
    :return: response
    :rtype: requests.Response
    """
    try:
        http_method = map_type_to_method(method)
        if "cookies" not in kwargs:
            kwargs['cookies'] = request.cookies.to_dict()
        logger.info(f"Try to proceed {method.upper()} request to {uri}")
        response = http_method(uri, **kwargs)
    except requests.RequestException as e:
        logger.exception(e)
        abort(HTTPStatus.SERVICE_UNAVAILABLE, f"{uri} is not available, try again later")

    if response.status_code == HTTPStatus.OK:
        return response
    logger.error(f"Error while {method.upper()} request to {uri}")
    logger.error(f"Response code: {response.status_code}")
    try:
        logger.error(json.dumps(response.json()))
    except Exception as e:
        logger.exception(e)
    if abort_status_code is None:
        abort_status_code = response.status_code
    abort(abort_status_code)
