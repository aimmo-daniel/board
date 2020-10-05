import datetime

import factory
from factory.mongoengine import MongoEngineFactory

from app.models.member import Member


class MemberFactory(MongoEngineFactory):
    class Meta:
        model = Member

    email = factory.Faker('email') # factory_boy -> faker
    name = factory.Faker('name')
    password = factory.Faker('password', length=30, special_chars=True, digits=True, upper_case=True, lower_case=True)
    created_time = factory.LazyAttribute(lambda _: datetime.datetime.utcnow())
    last_login_time = factory.LazyAttribute(lambda _: datetime.datetime.utcnow())
