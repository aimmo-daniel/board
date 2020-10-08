import factory
from factory.mongoengine import MongoEngineFactory

from app.models.member import Member


class MemberFactory(MongoEngineFactory):
    class Meta:
        model = Member

    email = factory.Faker('email')
    name = factory.Faker('name')
    password = factory.Faker('password', length=30, special_chars=True, digits=True, upper_case=True, lower_case=True)
    deleted = factory.LazyAttribute(lambda _: False)


class WithdrawalMemberFactory(MemberFactory):
    deleted = factory.LazyAttribute(lambda _: True)
