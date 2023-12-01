from bson import json_util
from mongoengine import connect, Document, StringField, ListField, ReferenceField, CASCADE

from connect import db, host

connect(db=db, host=host)

class Author1(Document):
    fullname = StringField(max_length=120, required=True, unique=True)
    born_date = StringField(max_length=50) # Поле строкове, а не дата
    born_location = StringField(max_length=150)
    description = StringField(required=True)
    meta = {"collection": "authors1"}


class Quote1(Document):
    author = ReferenceField('Author1', reverse_delete_rule=CASCADE)
    tags = ListField(StringField())
    quote = StringField(required=True)
    meta = {"collection": "quotes1"}

    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)


