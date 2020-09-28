import math

import mongoengine


class Pagination(object):
    # noinspection PyArgumentList
    def __init__(self, iterable, page, per_page, prefetch_related=None):
        if page < 1:
            page = 1

        self.iterable = iterable
        self.page = page
        self.per_page = per_page

        if isinstance(iterable, mongoengine.QuerySet):
            self.total = iterable.count()
        else:
            self.total = len(iterable)

        start_index = (page - 1) * per_page
        end_index = page * per_page

        self.items = iterable[start_index:end_index]
        if isinstance(self.items, mongoengine.QuerySet) and prefetch_related is not None:
            self.items = self.items.prefetch_related(*prefetch_related)

    @property
    def pages(self):
        return int(math.ceil(self.total / float(self.per_page)))