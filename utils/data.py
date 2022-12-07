import heapq


class PriorityQueue:
    """A subclass of Queue; retrieves entries in priority order (lowest first).
    Entries are typically tuples of the form: (priority number, data).
    """

    def __init__(self):
        self._queue = []

    def __bool__(self):
        return not self.empty()

    def put(self, item):
        heapq.heappush(self._queue, item)

    def get(self):
        return heapq.heappop(self._queue)

    def empty(self):
        return len(self._queue) == 0


def slice(text: str, chunk_size: int, overlap=0):
    while len(text) >= chunk_size:
        to_send, text = text[:chunk_size], text[chunk_size - overlap:]
        yield to_send
