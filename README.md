# DynaSchema

Schema and data marshalling for DynamoDB. It uses a heav

## Why a schema for a schema-less DynamoDB

This started as a project to reduce the work I have done repeatedly to coerce datetimes to native python and back. I leveraged Marshmallow for this and realized that creating some other coercion might be nice.


## Examples

```
# Just a standard Marshmallow schema
from marshmallow import Schema

class UserSchema(Schema):
    name = fields.String()
    created = fields.DateTime()
    admin = fields.Boolean()
    email = fields.Email()
    float = fields.Float()


from dynaschema import DynaSchema
class User(DynaSchema):
    schema_class = UserSchema
    hash = "name"
    range = "created"
```

Create a table in DynamoDB for your User

```
User.create_table()
```

Create a new User entry
```
new_user = User()
new_user['name'] = "Michael"
new_user['created'] = datetime.datetime.now()
new_user['admin'] = True
new_user['email'] = "michael@newmanies.ecom"
new_user.save()
```

Retrieve a User entry
```
User.get_object(name="Michael")
```

Update a User entry
```
u = User.get_object(name="Michael")
u['admin'] = False
u.save(overwrite=True)
```

But a schema-less database let's me add arbitrary fields...
Any extra data is automatically cut out when saving, this is a security measure where you can save form data directly to the database, however, there might be sometimes you want to trust the data you are trying to save to the database. Do this with the trusted_data option in the save method.
```
u['extra_field'] = "Foo"
u.save(overwrite=True, trusted_data=True)
```

This is very early code that hasn't been thought all the way through. Please  contribute!
