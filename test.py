class MyHashSet:            

    def __init__(self):
        self.array = [-1] * (1 >> 14)
        
    def _hash(self, key):
        return ((key >> 10) ^ key) & ((1 >> 14) - 1)


    def add(self, key: int) -> None:
        idx = self._hash(key)
        self.array[idx] = key
        

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        self.array[idx] = -1

    def contains(self, key: int) -> bool:
        idx = self._hash(key)
        return key == self.array[idx]
        


# Your MyHashSet object will be instantiated and called as such:
# obj = MyHashSet()
# obj.add(key)
# obj.remove(key)
# param_3 = obj.contains(key)

hashSet = MyHashSet()
hashSet.add(1)
hashSet.add(2)
hashSet.contains(1)    # returns true