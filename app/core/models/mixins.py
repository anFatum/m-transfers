from app import db
from sqlalchemy.exc import DatabaseError
from datetime import datetime
import json


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
    def to_json(self):
        fields = {}
        for field in [x for x in dir(self) if not x.startswith('_') and x != 'metadata']:
            data = self.__getattribute__(field)
            try:
                json.dumps(data)  # this will fail on non-encodable values, like other classes
                fields[field] = data
            except TypeError:
                if isinstance(data, JsonableMixin):
                    fields[field] = data.to_json()
                else:
                    fields[field] = None
        # a json-encodable dict
        return fields
