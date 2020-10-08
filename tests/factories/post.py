import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory

from app.models.post import Post
from tests.factories.board import BoardFactory
from tests.factories.member import MemberFactory


class PostFactory(MongoEngineFactory):
    class Meta:
        model = Post

    board = factory.SubFactory(BoardFactory)
    writer = factory.SubFactory(MemberFactory)
    title = fuzzy.FuzzyText(length=10, prefix='post_')
    content = fuzzy.FuzzyText(length=10, prefix='post_')
    #type = factory.LazyAttribute(lambda _: False)
    deleted = factory.LazyAttribute(lambda _: False)


class DeletedPostFactory(PostFactory):
    deleted = factory.LazyAttribute(lambda _: True)