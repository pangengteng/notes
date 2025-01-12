from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    
    def __repr__(self):
        return repr(self.val) + '->' + repr(self.next)

def insertSort(array:[int]): # type: ignore
    if len(array) == 0 or len(array) == 1:
        return
    for i in range(1, len(array)):
        value = array[i]
        for j in range(i-1, -1, -1):
            if array[j] < value:
                break
            array[j+1] = array[j]
        array[j+1] = value


# def selectionSort(array: Optional[int]):
#     for i in range(len(array)-1):
#         min_value = array[i]
#         for j in range(i+1, len(array)):
#             if array[j] < min_value:
#                 min_value, array[i], array[j] = array[j], array[j], min_value


# def selectionSort(head: Optional[ListNode]) -> Optional[ListNode]:
#     dummy = ListNode(next = head)
#     result = cur = ListNode()
    
#     while dummy.next:
#         p = dummy
#         i = j = dummy.next
#         min_value = i.val
#         while j.next:
#             if j.next.val < min_value:
#                 min_value = j.next.val
#                 p = j
#             j = j.next
        
#         node = p.next
#         p.next = p.next.next
#         node.next = None
#         cur.next = node
#         cur = cur.next

#     return result.next

def selectionSort(head: Optional[ListNode]) -> Optional[ListNode]:
    """ in-place implement """
    dummy = ListNode(next=head)

    p1 = dummy
    while p1.next:
        i = j = p2 = p1.next
        min_value = i
        while j.next:
            if j.next.val < min_value.val:
                min_value = j.next
                p2 = j
            j = j.next
        
        if i != min_value:
            k = p2.next
            p1.next, p2.next = k, i
            i.next, k.next = k.next, i.next
        
        p1 = p1.next
    
    return dummy.next

# listNode = ListNode(4, ListNode(2, ListNode(1, ListNode(3))))
# result = selectionSort(listNode)
# print(result)

import sys

def mergeSort(array:Optional[int]) -> Optional[int]:
    if len(array) == 0 or len(array) == 1:
        return array
    q = len(array) // 2
    
    # spilt
    left = mergeSort(array[:q])
    right = mergeSort(array[q:])

    # merge
    tmp = [None] * (len(left) + len(right))
    left.append(sys.maxsize)
    right.append(sys.maxsize)
    i = j = 0
    for k in range(len(tmp)):
        if left[i] < right[j]:
            tmp[k] = left[i]
            i += 1
        else:
            tmp[k] = right[j]
            j += 1
    return tmp


def quick_sort(array:Optional[int]):

    def _partition(array, start, end):
        pivot = array[end]
        i = 0
        for j in range(0, end):
            if array[j] < pivot:
                array[i], array[j] = array[j], array[i]
                i += 1
        array[i], array[end] = array[end], array[i]
        return i

    def _quick_sort(array:Optional[int], start: Optional[int], end: Optional[int]):
        if start >= end:
            return
        p = _partition(array, start, end)
        _quick_sort(array, start, p-1)
        _quick_sort(array, p, end)    

    _quick_sort(array, 0, len(array)-1)

array = [3, 2, 1, 4, 5]
quick_sort(array)
print(array)