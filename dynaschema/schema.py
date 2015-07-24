from copy import deepcopy

from boto.dynamodb2.items import Item
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from .fields import get_dynamo_type


class TableAlreadyExists(Exception):
    pass

class DynaIndex():
    def __init__(self, hash=None, range=None):
        self.hash = hash
        self.range = range

class DynaSchema(dict):
    schema_class = None
    dump_schema_class = None
    hash = None
    range = None
    dynamo_connection = None

    def __init__(self, dynamo_item=None):
        if not dynamo_item:
            dynamo_item = Item(self.get_dyna_table())
        else:
            # ensure the dynamo item is a dict
            data = dict(dynamo_item)

            print dir(self.schema_class)

            data, errors = self.get_schema().load(data)

            if errors:
                raise AttributeError(errors)
            self.update(data)

        self.dynamo_item = dynamo_item

    def get_schema(self):
        return self.schema_class()

    def get_dump_schema(self):
        return (self.dump_schema_class or self.schema_class)()

    def get_hash_field(self):
        return self.hash_field

    def get_range_field(self):
        return self.range_field

    @classmethod
    def get_dyna_table(cls):
        return Table(cls.__name__, connection=cls.dynamo_connection)

    @classmethod
    def create_table(cls, connection=None):

        if not cls.schema_class:
            raise AttributeError("Must define a schema to auto create index")

        dynaschema = cls.schema_class()

        if cls.hash:
            schema = [
                HashKey(cls.hash, data_type=get_dynamo_type(dynaschema.fields[cls.hash])),
            ]
        else:
            raise AttributeError("Must have a hash_field defined")

        if cls.range:
            schema.append(RangeKey(cls.range, data_type=get_dynamo_type(dynaschema.fields[cls.range])))

        if cls.__name__ in connection.list_tables().get("TableNames", []):
            raise TableAlreadyExists("A table with the name %s already exists" % cls.__name__)
        return Table.create(cls.__name__, schema=schema, connection=connection)
        #TODO: Add Throughput
        #TODO: Add Indexes

    def save(self, trusted_data=False, overwrite=False):
        if trusted_data:
            schema = self.get_schema()
            schema.fields = self.keys()
            data, errors = schema.dump(self)
        else:
            data, errors = self.get_schema().dump(self)

        if errors:
            raise AttributeError(errors)

        for k,v in data.items():
            self.dynamo_item[k] = v

        return self.dynamo_item.save(overwrite=overwrite)

    def dump(self):
        return self.get_dump_schema().dump(self).data

    @classmethod
    def get_object(cls, **kwargs):
        #TODO assert kwargs is only len2 and might match indexes
        schema = cls.schema_class(only=kwargs.keys())
        kwargs, errors = schema.dump(kwargs)
        if errors:
            raise AttributeError(errors)

        item = cls.get_dyna_table().get_item(**kwargs)
        return cls(dynamo_item=item)

    @classmethod
    def get_or_create(cls, **kwargs):
        schema = cls.schema_class(only=kwargs.keys())
        kwargs, errors = schema.dump(kwargs)
        if errors:
            raise AttributeError(errors)

        try:
            item = cls.get_dyna_table().get_item(**kwargs)
        except exceptions.ItemNotFound:
            new_cls = cls()
            new_cls.update(kwargs)
            return new_cls, True
        else:
            return cls(dynamo_item=item), False
