def sort_array(nums: list[int]) -> list[int]:
    """
    Моя реализация сортировки подсчётом.
    :param nums:
    :return:
    """
    result = []
    sorted_ = dict((i, 0) for i in range(min(nums), max(nums) + 1))
    for i in nums:
        sorted_[i] += 1
    for i in sorted_:
        result += [i] * sorted_[i]
    return result
