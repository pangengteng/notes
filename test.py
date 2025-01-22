from typing import List


def first_index_of(array, value):
    low, high = 0, len(array) - 1
    while low <= high:
        mid = low + ((high - low) >> 1)
        if array[mid] >= value:
            high = mid - 1
        else:
            low = mid + 1
    
    if low < len(array) and array[low] == value:
        return low
    
    return -1


def last_index_of(array, value):
    low, high = 0, len(array) - 1
    while low <= high:
        mid = low + ((high - low) >> 1)
        if array[mid] <= value:
            low = mid + 1
        else:
            high = mid - 1
    if high >= 0 and array[high] == value:
        return high
    return -1


def first_gt_index_of(array, value):
    low, high = 0, len(array) - 1
    while low <= high:
        mid = low + ((high - low) >> 1)
        if array[mid] >= value:
            high = mid - 1
        else:
            low = mid + 1
    if low < len(array):
        return low
    return -1


def last_lt_index_of(array, value):
    low, high = 0, len(array) - 1
    while low <= high:
        mid = low + ((high - low) >> 1)
        if array[mid] <= value:
            low = mid + 1
        else:
            high = mid - 1
    if high >= 0:
        return high
    return -1

def insert_index_of(array, value):
    low, high = 0, len(array) - 1
    while low <= high:
        mid = low + ((high - low) >> 1)
        if array[mid] <= value:
            low = mid + 1
        else:
            high = mid - 1
    if low < len(array):
        return low
    return -1 # all of elements smaller or equals than value

print(first_index_of([1, 2, 3, 3, 3, 3, 4, 5], 3))  # 2
print(last_index_of([1, 2, 3, 3, 3, 3, 4, 5], 3))  # 5
print(first_gt_index_of([1, 2, 3, 3, 3, 3, 4, 5], 3))  # 2
print(last_lt_index_of([1, 2, 3, 3, 3, 3, 4, 5], 3))  # 5
print(insert_index_of([1, 2, 3, 3, 3, 3, 4, 5], 3))  # 6