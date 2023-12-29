from bson.errors import InvalidId
from bson.objectid import ObjectId as BsonObjectId


class ObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return cls(v)
        except InvalidId:
            raise ValueError(f"{v} is not a valid ObjectId")

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
