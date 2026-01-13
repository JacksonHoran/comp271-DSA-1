#COMP 271
'''
Assignment name:  Week 10, Binary Search
LUC id and Name:  Jhoran1@luc.edu
Date:             10/2/25
'''

####Questions for grader
'''
None 
'''
###### Assignment description
'''
write a binary search algorithm that tracks the number of occurances of a given number in a sorted list of integers.
'''

'''
low <- 0
high <- last index
result <- None

while low is less than or equal to high
    mid <- middle index

    if mid index is the target
        result <- mid
        hugh <- mid -1
    elif mid index less than target value
        low <- mid + 1
    else:
        high <- mid + 1
    
    return result
'''
def leftMost(values: list[int], target: int) -> int | None:
    '''Finds the leftmost occurrance of a given value in a sorted list of integers.'''
    low = 0
    high = len(values) - 1
    result = None
    
    while low <= high:
        mid = (low+high) // 2

        if values[mid] == target:
            result = mid
            high = mid - 1
        elif values[mid] < target:
            low = mid + 1
        else:
            high = mid -1

    return result

'''
low <- 0
high <- last index
result <- None

while low is less than or equal to high
    mid <- middle index

    if mid index is the target
        result <- mid
        low <- mid -1
    elif mid index less than target value
        low <- mid + 1
    else:
        high <- mid + 1
    
    return result
'''
def rightMost(values: list[int], target: int) -> int | None:
    '''Finds the rightmost value in a sorted list of integers.'''
    low = 0
    high = len(values) - 1
    result = None
    
    while low <= high:
        mid = (low+high) // 2

        if values[mid] == target:
            result = mid
            low = mid +1
        elif values[mid] < target:
            low = mid + 1
        else:
            high = mid -1

    return result

'''
left <- leftmost(values, target)
right <- rightmost(values, target)
occurs <- int

if left or right is none:
    no occurances
else:
    find difference in left and right indecies and add one

return occurs
'''
def occurrences(values: list[int], target: int) -> int | None:
    '''Returns the number of occurrences of a given integers in a sorted list using binary search.'''
    left = leftMost(values, target)
    right = rightMost(values, target)
    occurrs: int

    if left is None or right is None:
        occurrs = 0
    else:
        occurrs = right - left + 1

    return occurrs


'''
create ordered integet list
print occurences(list, num)
'''
def main():
    list = [1,2,2,2,2,3,4,5,5,5,5,5,6,7,8,9,10]
    print(occurrences(list, 2))

main()