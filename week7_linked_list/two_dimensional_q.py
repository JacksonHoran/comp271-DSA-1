#COMP 271
'''
Assignment name:  Take home Midterm
LUC id and Name:  Jhoran1@luc.edu
Date:             10/6/25
'''

####Questions for grader
'''
No questions but i want to make it clear that there was one line of code that i got help from StackOverflow.
i wanted to print the raw array in a 'matrix' fasion and i could not figure out how to print the matrix this way
inside the f string i used to return the attributes of the class in the __str__ method. 
'''
###### Assignment description
'''
Create a 2d list queue with O(1) enqueue, dequeue, and peek methods.
'''
###### A. Problem Decomposition:
'''
We need to figure out how to enqueue, dequeue, peek, and update the front and back values of the queue in O(1) time.
This means that we cannot shoft the values left or right, rather well keep every item in the same index for their entire 
time in the queue. We will keep a front and rear index and update them accordingly everytime a new value is
added or removed from the queue.
'''
###### B. Program architecture:
'''
Class initalizer
    takes an integer n to determine "n x n" size of array

__str__()
    takes self
    returns the class attributes in a user friendly format
    (implemented for testing purposes)

__repr__()
    takes self
    returns a string representation of the object, for developers not users.

__bool__()
    takes self
    returns true if the queue is being used, false if empty or full

Getters
    getCapacity()
    getUsage()

Private Helpers
    -isFull()
        returns true if array is full, false otherwise
    -isEmpty()
        returns true if array is empty, false otherwise
    -update()
        increments front or back index
    -rowAndCol()
        returns the front or back index

Core
    enqueue()
        takes a string, appends to the back of the queue with O(1). Returns false if the queue is full
    dequeue()
        removes and returns the front item from the queue with O(1). returns None if the queue is empty.
    peek()
        returns front item with O(1).
    list_queue()
        returns a 1d list of the queue in logical order.
    
Testing
'''

class TwoDimensionalQ:
    def __init__(self, n: int = 4):
        self._underlying: list[list[str]] = [[None for _ in range(n)] for _ in range(n)]
        self._n: int = n
        self._capacity: int = n * n
        self._usage: int = 0
        self._front_row: int = 0
        self._front_col: int = 0
        self._back_row: int = 0
        self._back_col: int = 0
    
    def __str__(self) -> str:
        '''Returns the class attributes in a user-friendly format.
        
        Sources: https://stackoverflow.com/questions/54230650/joining-printing-characters-into-a-string-from-a-2d-array'''
        matrix = "\n ".join(" ".join(str(i) for i in row) for row in self._underlying)
        return (
            f"\nUnderlying Matrix:\n\n {matrix}\n"
            f"\nDimensions: {self._n} x {self._n}"
            f"\nCapacity: {self.getCapacity()}"
            f"\nUsage: {self.getUsage()}"
            f"\nFront Position: ({self._front_row}, {self._front_col})"
            f"\nBack Position: ({self._back_row}, {self._back_col})"
            )
    
    def __repr__(self) -> str:
        '''Returns string representation of object.'''
        return f"TwoDimensionalQ(n = {self._n})"
    
    def __bool__(self) -> bool:
       '''Returns True if queue is not empty or full. Otherwise returns False.'''
       status: bool = True
       if self.__isEmpty() or self.__isFull():
           status = False
       return status

    # Getters
    def getCapacity(self) -> int:
        '''Returns queue capacity.'''
        return self._capacity
    
    def getUsage(self) -> int:
        '''Returns queue usage.'''
        return self._usage

    # Private helpers
    def __isFull(self) -> bool:
        '''Returns True is the queue is full, False otherwise.'''
        return self.getCapacity() == self.getUsage()
    
    def __isEmpty(self) -> bool:
        '''Returns True if the queue is empty, False otherwise.'''
        return self.getUsage() == 0
    
    '''Core logic for this method is the exact same for each segment of the if statement, however the if 
    statement determines whether we are updating the front or back of the queue
    
    The logic is as follows:
        decrement/increment usage
        collumn plus one mod n
        IF collumn is 0
            row plus one mod n
        
        IF the method is not passed 'enqueue' or 'dequeue' a value error is raised.'''
    def __update(self, side: str) -> None:
        '''Increments the front or back with wrap using modular arithmatic'''
        if side == 'dequeue':
            self._usage -= 1
            self._front_col = (self._front_col + 1) % self._n
            if self._front_col == 0:
                self._front_row = (self._front_row + 1) % self._n
        elif side == 'enqueue':
            self._usage += 1
            self._back_col = (self._back_col + 1) % self._n
            if self._back_col == 0:
                self._back_row = (self._back_row + 1) % self._n
        else:
            raise ValueError

    '''IF function is passed 'enqueue'
            row is set to back row, and col is set to back collumn
        ELIF function is passed 'dequeue'
            row is set to front row, and col us set to back collumn
        ELSE
            raise a value error
        RETURN row and col'''
    def __rowAndCol(self, side: str) -> int:
        '''Returns the index of the front or back of the queue.'''
        if side == 'enqueue':
            row, col = self._back_row, self._back_col
        elif side in ('dequeue', 'front'):
            row, col = self._front_row, self._front_col
        else:
            raise ValueError
        return row, col
        
    # Core
    '''
    call rowAndCol helper with parameter 'enqueue'
    create local bool 'success'
    IF capacity is equal to usage
        success is set to False
    ELSE
        back position is set to value parameter
        success is set to True
        call update with prameter 'enqueue'
    RETURN success
        '''
    def enqueue(self, value: str) -> bool:
        '''Appends item at the back of the queue. Returns False if queue is empty.'''
        row, col = self.__rowAndCol('enqueue')
        success: bool
        if self.getCapacity() == self.getUsage():
            success = False
        else:
            self._underlying[row][col] = value 
            success = True
            self.__update('enqueue')
        return success
    
    '''
    set local variable 'item' to None
    IF usage is equal to 0
        call rowAndCol with parameter 'dequeue'
        item is set to value at the front of the queue
        front position in queue is set to None
        call update with parameter dequeue
    RETURN item'''
    def dequeue(self) -> str | None: 
        '''Removes and returns item at the front of the queue. returns none if queue is empty.''' 
        item = None
        if self.getUsage() > 0:
            row, col = self.__rowAndCol('dequeue')
            item = self._underlying[row][col]
            self._underlying[row][col] = None
            self.__update('dequeue')
        return item 

    '''
    call rowAndCol with parameter 'front'
    set local variable item to the value at the front of the queue
    RETURN item'''
    def peek(self) -> str | None:
        '''Constant time look at front value.'''
        row, col = self.__rowAndCol('front')
        item = self._underlying[row][col]
        return item

    '''
    create local list 'list_queue'
    create integer count
    create local integers row and col set to rowAndCol with parameter 'front'
    WHILE count is less than usage
        IF position at [row][col] is not none
            append the value to list_queue
        increment count
        col plus one mod n
        IF col is 0
            row plus one mod n
        RETURN list_queue'''
    def list_queue(self) -> list[str]:
        '''Returns the queue in a logically ordered list.'''
        list_queue = []
        count = 0
        row, col  = self.__rowAndCol('front')
        while count < self.getUsage():
            if self._underlying[row][col] != None:
                list_queue.append(self._underlying[row][col])
            count += 1
            col = (col + 1) % self._n
            if col == 0:
                row = (row + 1) % self._n
        return list_queue
                
if __name__ == "__main__":
    '''To test the queue, i sort of simulated how a doctors office might work. a few people come in and
    begin to wait, then a couple are called back, some more come in, maybe one is taken back. Then before
    you know it the waiting room is full. Someone tries to come in and wait but the room is full. By the end 
    of the day no more patients are scheduled and everyone is brought back for their appointment, the queue
    is emptied. After each modification to the queue i called the __str__ method to show all the attributes 
    and the visual representation of the array or seating matrix. I did to show that the logic is tracking
    the positions correctly and to show that the enqueue and dequeue methods use an O(1) algorithm.'''
    q = TwoDimensionalQ(n=3)
    print("---empty---")
    print(q)
    print(f"Current usage status(true = in use, false = not in use or full): {bool(q)}\n")
    print("---enqueued 5 people---")
    group1 = ['carson', 'spencer', 'ledyn', 'ike', 'max']
    for item in group1:
        print(f'{item} has joined the queue.')
        q.enqueue(item)
    print(q)
    print(f"\nLogical Queue as list: {q.list_queue()}\n")
    print(f"Current usage status(true = in use, false = not in use or full): {bool(q)}\n")
    print("---dequeued 2 people---")
    q.dequeue()
    q.dequeue()
    print(q)
    print(f"\nLogical Queue as list: {q.list_queue()}\n")
    print(f"Current usage status(true = in use, false = not in use or full): {bool(q)}\n")
    print("---enqueued 3 people---")
    group2 = ['jack', 'brett', 'kate']
    for item in group2:
        print(f'{item} has joined the queue.')
        q.enqueue(item)
    print(q)
    print(f"\nLogical Queue as list: {q.list_queue()}\n")
    print(f"Current usage status(true = in use, false = not in use or full): {bool(q)}\n")
    print("---peek---")
    print(q.peek())
    print("---enqueued 3 people---")
    group3 = ['anton', 'danny', 'miles']
    for item in group3:
        print(f'{item} has joined the queue.')
        q.enqueue(item)
    print(q)
    print(f"\nLogical Queue as list: {q.list_queue()}\n")
    print(f"Current usage status(true = in use, false = not in use or full): {bool(q)}\n")    
    print("---enqueued 1 person---")
    q.enqueue("jake")
    print(q)
    print(f"\nLogical Queue as list: {q.list_queue()}\n")
    print("---empty the queue---")
    for i in range(0,9):
        q.dequeue()
    print(q)
    print(f"\nLogical Queue as list: {q.list_queue()}\n")
    print(f"Current usage status(true = in use, false = not in use or full): {bool(q)}\n")    



    
