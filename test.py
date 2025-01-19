from typing import List


class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        nums = self.merge_sort(nums)
        return nums[-k]
    
    def merge_sort(self, nums):
        if len(nums) == 0 or len(nums) == 1:
            return nums
        
        p = len(nums) // 2

        left = self.merge_sort(nums[:p])
        right = self.merge_sort(nums[p:])
        return self.merge(left, right)
    
    def merge(self, left, right):
        if left[-1] <= right[0]:
            return left + right
        
        tmp = [None] * (len(left) + len(right))
        left.append(float('inf'))
        right.append(float('inf'))
        i = j = 0
        for k in range(len(tmp)):
            if left[i] <= right[j]:
                tmp[k] = left[i]
                i += 1
            else:
                tmp[k] = right[j]
                j += 1
        return tmp
            

print(Solution().findKthLargest([3,2,1,5,6,4], 2))