import datetime

from boto.dynamodb2.layer1 import DynamoDBConnection

from boto.dynamodb2 import exceptions
from boto.dynamodb2.items import Item
from boto.dynamodb2.table import Table

from dynaschema import DynaSchema, Schema
from dynaschema.schema import TableAlreadyExists
from dynaschema import fields

import time

class UserSchema(Schema):
    name = fields.String()
    created = fields.DateTime()
    admin = fields.Boolean()
    email = fields.Email()
    float = fields.Float()

class User(DynaSchema):
    schema_class = UserSchema
    hash = "name"
    range = "created"


class TestDatabaseObject:

    def setUp(self):
        conn = DynamoDBConnection(
            host='localhost',
            port=8000,
            aws_access_key_id='anything',
            aws_secret_access_key='anything',
            is_secure=False)

        User.dynamo_connection = conn

        try:
            User.create_table(connection=conn)
        except TableAlreadyExists:
            pass

        self.now = datetime.datetime.now()

        self.u = User()
        self.u['name'] = "Michael"
        self.u['created'] = self.now
        self.u['admin'] = True
        self.u['email'] = "michael@newmanies.ecom"
        self.u.save()

    def teardown(self):
        User.get_dyna_table().delete()

    def test_retrieval(self):
        u = User.get_object(name="Michael", created=self.now)
        u['email'] == "michael@newmanies.ecom"

    def test_update(self):
        u = User.get_object(name="Michael", created=self.now)
        u['admin'] = False
        u['email'] == "michael@newmanies.ecom"

        u.save(overwrite=True)

        u = User.get_object(name="Michael", created=self.now)
        u['admin'] == False

    def test_datetime_serialization(self):
        u = User.get_object(name="Michael", created=self.now)
        u['created'] == self.now

    def test_additional_field(self):
        self.u['extra_field'] = "Hello World"
        self.u.save(overwrite=True)

        u = User.get_object(name="Michael", created=self.now)
        u.get('extra_field') == None

    def test_trusted_data(self):
        self.u['extra_field'] = "Hello World"
        self.u.save(overwrite=True, trusted_data=True)

        u = User.get_object(name="Michael", created=self.now)
        u.get('extra_field') == "Hello World"


    def test_float_accuracy(self):
        u = User.get_object(name="Michael", created=self.now)
        # u['float'] = float(99.9)
        u.save(overwrite=True)

    def test_set(self):
        pass
