import factory
from factory.mongoengine import MongoEngineFactory

from app.models.comment import Comment


class CommentFactory(MongoEngineFactory):
    class Meta:
        model = Comment


class DeletedCommentFactory(CommentFactory):
    deleted = factory.LazyAttribute(lambda _: True)