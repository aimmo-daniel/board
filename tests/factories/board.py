import factory
from factory import fuzzy
from factory.mongoengine import MongoEngineFactory

from app.models.board import Board


class BoardFactory(MongoEngineFactory):
    class Meta:
        model = Board

    name = fuzzy.FuzzyText(length=10, prefix='board_')
    deleted = factory.LazyAttribute(lambda _: False)


class DeletedBoardFactory(BoardFactory):
    deleted = factory.LazyAttribute(lambda _: True)