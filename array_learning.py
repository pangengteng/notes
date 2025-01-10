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

array = [3, 2, 1, 4, 5]
insertSort(array)
print(array)