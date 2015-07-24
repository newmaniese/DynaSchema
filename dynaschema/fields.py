from marshmallow import fields
from marshmallow.fields import String, Date, DateTime, Email, URL, UUID, LocalDateTime, Time, TimeDelta
from marshmallow.fields import Boolean
from marshmallow.fields import Integer, Decimal, Number, Float
from marshmallow.fields import List, Nested

from boto.dynamodb2.types import STRING, NUMBER, BINARY, STRING_SET, NUMBER_SET, BINARY_SET, NULL, BOOLEAN, MAP, LIST


FIELD_TO_DYNAMO_TYPE_MAPPING = {
    String : STRING,
    Date : STRING,
    DateTime : STRING,
    Email : STRING,
    URL : STRING,
    UUID : STRING,
    LocalDateTime : STRING,
    Time : STRING,
    TimeDelta : STRING,
    Boolean : BOOLEAN,
    Integer : NUMBER,
    Decimal : NUMBER,
    Number : NUMBER,
    Float : NUMBER,
    List : LIST,
    Nested : MAP,
}

OUTPUT_TO_DYNAMO_TYPE_MAPPING = {
    str : STRING,
    unicode : STRING,
    bytes : BINARY,
    int : NUMBER,
    None : NULL,
    Boolean : BOOLEAN,
    dict : MAP,
    list : LIST,
}

def get_dynamo_type(field):
    t = FIELD_TO_DYNAMO_TYPE_MAPPING.get(field.__class__)
    if t:
        return t

    for field_type, t in FIELD_TO_DYNAMO_TYPE_MAPPING.items():
        if isinstance(field, field_type):
            return t

class SetField(fields.Field):
    #TODO: This should have a property defining the type of the set, then it defines the dyna_type from that
    dyna_type = STRING_SET
    def _serialize(self, value, attr, obj):
        return set(super(SetField, self)._serialize(list(value), attr, obj))

    def _deserialize(self, value):
        if not (isinstance(value, list) or isinstance(value, set)):
            value = value.split(",")
        return set(super(SetField, self)._deserialize(list(value)))
