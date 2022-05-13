from app import db
from sqlalchemy.exc import DatabaseError
from datetime import datetime
import json
from typing import Iterable
from six import string_types
from app.core.utils.iterable_utils import delete_none_keys

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.now())


class SaveableModelMixin:
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except DatabaseError as e:
            return {"err": e.detail}


class JsonableMixin:
    def to_json(self, recursive=True):
        fields = {}
        for field in [x for x in dir(self) if not x.startswith('_') and x != 'metadata' and x != 'query']:
            data = self.__getattribute__(field)
            try:
                if isinstance(data, datetime):
                    fields[field] = data.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
            except TypeError:
                fields[field] = None
                if recursive:
                    if isinstance(data, JsonableMixin):
                        fields[field] = data.to_json()
                    elif isinstance(data, Iterable) and not isinstance(data, string_types) \
                            and not callable(data):
                        fields[field] = [val.to_json(recursive=False)
                                         for val in data if isinstance(val, JsonableMixin)]
        # a json-encodable dict
        return delete_none_keys(fields)
