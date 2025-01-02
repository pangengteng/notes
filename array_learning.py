# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def addTwoNumbers(l1, l2):
    """
    :type l1: Optional[ListNode]
    :type l2: Optional[ListNode]
    :rtype: Optional[ListNode]
    """
    head = None
    current = None
    over_bit = 0
    while True:
        if l1 is None:
            l1_val = 0
        else:
            l1_val = l1.val

        if l2 is None:
            l2_val = 0
        else:
            l2_val = l2.val

        val = l1_val + l2_val + over_bit
        if val > 10:
            val = val - 10
            over_bit = 1
        else:
            over_bit = 0

        if head is None:
            head = ListNode(val)
            current = head
        else:
            current.next = ListNode(val)
            current = current.next
        
        if l1 is None and l2 is None and over_bit == 0:
            break

        if l1 is not None:
            l1 = l1.next
        
        if l2 is not None:
            l2 = l2.next
    
    return head



def createNode(val):
    head = None
    current = None
    for v in val:
        if head is None:
            head = ListNode(v)
            current = head
        else:
            current.next = ListNode(v)
            current = current.next
    return head

n1 = createNode([2,4,3])
n2 = createNode([5,6,4])

print(addTwoNumbers(n1, n2))