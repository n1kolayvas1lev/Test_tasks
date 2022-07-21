# coding=utf-8
from collections import deque


class CircularBuffer(deque):
    """
    Класс реализующий кольцевой буфер.
    """
    def __init__(self, size):
        super(CircularBuffer, self).__init__(maxlen=size)
        self.size = size

    def __str__(self):
        return 'circular_buffer:[' + ','.join(map(str, self)) + ']'

    def add_item(self, other, return_flag=False, overwrite=True):
        """
        Добавление элемента в буфер.
        :param other: Any Добавляемый элемент.
        :param return_flag: bool Нужно ли возвращать заменяемые элементы при добавлении новых
        :param overwrite: bool Нужно ли перезаписывать элементы при добавлении новых.
        :return: Optional[Any]
        """
        if len(self) == self.size:
            if overwrite:
                result = self[0]
                self.append(other)
                if return_flag:
                    return result
            else:
                raise Exception('Buffer is full.')
        else:
            self.append(other)


if __name__ == '__main__':
    cb = CircularBuffer(5)
    for i in xrange(100):
        print cb.add_item(i, return_flag=True)
        print cb
    print type(cb)
    print cb.popleft()
    print cb

