from typing import Optional, Any


class CircularBuffer:
    """
    Класс реализующий кольцевой буфер.
    """
    def __init__(self, size: int):
        self.__buffer = [None] * size
        self.__length = size
        self.__busy = 0
        self.__head = 0
        self.__tail = 0

    def __shift_tail(self) -> None:
        """
        Смещение индекса первого пришедшего элемента
        :return: None
        """
        self.__tail = (self.__tail + 1) % self.__length

    def add_item(self, other: Any, return_flag=False, overwrite=True) -> Optional[Any]:
        """
        Добавление элемента в буфер.
        :param other: Any Добавляемый элемент.
        :param return_flag: bool Нужно ли возвращать заменяемые элементы при добавлении новых
        :param overwrite: bool Нужно ли перезаписывать элементы при добавлении новых.
        :return: Optional[Any]
        """
        result = None
        if self.__busy == self.__length:
            if overwrite:
                self.__shift_tail()
                if return_flag:
                    result = self.__buffer[self.__head]
            else:
                raise Exception('Buffer is full.')
        else:
            self.__busy += 1
        self.__buffer[self.__head] = other
        self.__head = (self.__head + 1) % self.__length
        return result

    def remove_item(self) -> Optional[Any]:
        """
        Удаление объектов из буфера по FIFO.
        :return: Optional[Any]
        """
        if self.__busy:
            result = self.__buffer[self.__tail]
            self.__shift_tail()
            self.__busy -= 1
            return result
        else:
            raise Exception('Empty buffer.')

    def __repr__(self):
        return '[' + ','.join(map(str, self.__buffer)) + ']'

    def __str__(self):
        return 'cb:[' + ','.join(map(lambda x: str(x) if x is not None else '', self.__buffer)) + ']'

    def __len__(self):
        return self.__busy

    def __iter__(self):
        while self.__busy > 0:
            yield self.__buffer[self.__tail]
            self.__shift_tail()
            self.__busy -= 1


if __name__ == '__main__':
    cb = CircularBuffer(10)
    for i in range(100):
        cb.add_item(i)

        print(cb)
    # for i in cb:
    #     print(i)
    for i in range(len(cb)):
        cb.remove_item()
        print(cb)
