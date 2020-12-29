class list_iterator():
    def __init__(self, collection, cursor):
        self._collection = collection
        self.cursor = cursor

    def first(self):
        self.cursor = -1

    def next(self):
        if self.cursor + 1 >= len(self._collection):
            raise StopIteration()
        self.cursor += 1

    def current(self):
        return self._collection[self.cursor]

