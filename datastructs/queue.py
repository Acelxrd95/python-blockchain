class Queue:
    def __init__(self, *args):
        self._queuelist = []

    def __len__(self):
        return len(self._queuelist)

    def enqueue(self, *args):
        for arg in args:
            self._queuelist.append(arg)

    def dequeue(self):
        return self._queuelist.pop()
