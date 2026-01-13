#COMP 271
'''
Assignment name:  Hashing and Lists
LUC id and Name:  Jhoran1@luc.edu
Date:             10/18/25
'''

####Questions for grader
'''
None
'''
###### Assignment description
'''
Implement a remove method as well as an exists method that removes and returns an item in the 'hotel' or
returns whether an item exists in the 'hotel' respectively.
'''
###### A. Problem Decomposition:
'''
The one major problem i ran into when implementing these methods was within the remoes method. I couldn't
figure out how to iteratre through the singly linked list and updating the pointer of the previous 
item when removing from the middle. I tried had a fair amount of ideas, one specifically was that i could 
remove the given item and then reierate through the linked list, find the gap and address it accordingly.
However this obviously wont work if you give it the least bit of thinking. Reason one is that it would be
extremely slow, you would hjave to iterate the liste twice which is not ideal, additionaly, when you reach
the node that points to a gap, you now no longer are able to reach any more items in the list because the
only way to get to the next is through a viable pointer. So if you remove item number 4, you need to update
the pointer of item 3 to item 5, however the only way to access number 5 is through number 4 which you just
deleted. 

So instead of trying to implement that dumb idea, i recalled one of the strategies we used on an assignment 
a week or two ago where we had a slow counter and a fast counter, i did something similar. I used a current
previous variable inside a while loop. So the algorithm starts at the head of the linked list and the previous 
is set to None. Inside a while loop i check a number different scenarios but essentially, if the current node
has the same name as the one passed to the function i remove it by setting the pointer of previous to current.next
Then adjust size and usage accordingly. There are two sort of edge cases here that i also had to think about.
One being is the linked list only has one node, the room is just set to None. The other is if the person 
leaving is at the head of the list we just set the head to current.next since there is no previous node.

One other small thing i decided to add was an if statement in the remove function. Essentially before beginning
any tasks from the removal algorithm, we check if the guest even exists in the list. That way if a user types
the wrong name, or is given false information and tries to remove a non existant guest the program is a little
bit faster. If i were seriously implemnenting this in real software i would probably have added something to inform
the user that they tried to remove a guest that is not currently staying in the hotel.
'''

# UPDATED: Oct 16 Added self._size = 0 in `_rehash`
from Guest import Guest    # UPDATED: Oct 15

class HotelAlphabetical:
    """Class representing a hotel where guests are stored in rooms based on
    the first initial of their names. Each room is a linked list of guests.
    """

    _DEFAULT_CAPACITY = 26
    _ASCII_LEFT_EDGE = ord("A")
    _ASCII_RIGHT_EDGE = ord("Z")
    _EMPTY = "boohoo, your hotel is empty."
    _NEXT_GUEST = " --> "

    _LOAD_FACTOR_THRESHOLD = 0.7
    _INCREMENT_FACTOR = 2

    def __init__(self, capacity: int = _DEFAULT_CAPACITY):
        self._capacity = capacity
        self._hotel = [None] * capacity  # Array of linked lists for each letter
        self._usage = 0  # number of array slots used
        self._size = 0

    def _get_index(self, name: str) -> int:
        """Compute the index in the hotel array based on the first
        initial of the guest's name."""
        # Default to 0 if name is None or empty or not A-Z
        room_index = 0
        if name is not None and len(name) > 0:
            # DISCUSSION POINT: should we be computing the first initial
            # here or should it be done in object Guest?
            initial_ascii = ord(name.upper()[0])
            if self._ASCII_LEFT_EDGE <= initial_ascii <= self._ASCII_RIGHT_EDGE:
                room_index = initial_ascii % self._capacity
        return room_index

    def _check_load_factor(self) -> bool:
        """Check if the load factor exceeds the threshold."""
        load_factor = self._usage / self._capacity
        return load_factor > self._LOAD_FACTOR_THRESHOLD

    def _rehash(self) -> None:
        """Rehash the hotel by increasing its capacity and reassigning guests."""
        # Preserve the old hotel array and its capacity
        old_hotel = self._hotel
        old_capacity = self._capacity
        # Create a new hotel array with increased capacity
        self._capacity *= self._INCREMENT_FACTOR
        # Initialize the new hotel array and reset usage
        self._hotel = [None] * self._capacity
        self._usage = 0
        self._size = 0       # UPDATE Oct 16
        # Reinsert all guests into the new hotel array
        for room in range(old_capacity):
            guest_in_room = old_hotel[room]
            while guest_in_room is not None:
                self.add_guest(guest_in_room.get_name())
                guest_in_room = guest_in_room.get_next()

    def add_guest(self, name: str) -> None:
        """Add a guest to the hotel."""
        if self._check_load_factor():
            self._rehash()
        # Compute the room index based on the first initial of the name
        room = self._get_index(name)
        # Create a new guest object
        guest = Guest(name)
        # Insert the guest at the front of the linked list for that room
        if self._hotel[room] is None:
            self._hotel[room] = guest
            self._usage += 1
        else:
            guest.set_next(self._hotel[room])
            self._hotel[room] = guest
        # Increment the current occupancy of the hotel
        self._size += 1


    def exists(self, guest_name:str) -> bool:
        '''returns true if a guest exists in the hotel'''
        # bool 'exists' is set to false to ensure one return statement
        # Get the room correspondiong to the guest name
        # set guests equal to the linked list for ease of iterating
        exists = False
        room = self._get_index(guest_name)
        guests = self._hotel[room]

        # while the corresponding room is not empty 
        while guests is not None and not exists:
            # if the current node in the room is equal to the guest in question
            if guests.name == guest_name:
                # exists bool is set to true
                exists = True
            # if the current node was not equal to the guest in question
            else:
                # the current guest is set to the next guest in the linked list
                guests = guests.get_next()
        # returns wehther or not the guest is present in the list or not
        return exists

    def remove(self, guest_name:str) -> Guest | None:
        '''removes and returns a particular guest from the hotel.'''
        # bool 'guestLeaving' is set to None to ensure one return statement
        # Get the room correspondiong to the guest name
        guestLeaving = None
        room = self._get_index(guest_name)
        # If the guest is present in the hotel, continue with the remove algorithm.
        if self.exists(guest_name):
            # begin current and previous node counters/pointers
            currentGuest = self._hotel[room]
            previousGuest = None

            # while there is still stuff to iterate and the leaving guest hasnt been found
            while currentGuest is not None and guestLeaving is None:
                # if the current gust is the one leaving
                if currentGuest.name == guest_name:
                    # mark them as the guest leaving
                    guestLeaving = currentGuest
                    # if we're at the head of the list
                    if previousGuest == None:
                        # set the head to the next node
                        self._hotel[room] = currentGuest.get_next()
                        # if the list was only one node, the room is None
                        if self._hotel[room] is None:
                            # decrement usage and size
                            self._usage -= 1
                            self._size -= 1
                    # if we arent at the head of the list
                    else:
                        # set the "next" pointer of previous node to currents next pointer
                        # essentially removing current node and shifting the next pointers back one position
                        previousGuest.set_next(currentGuest.get_next())
                        # only increment size 
                        self._size -= 1
                # if the leaving guest wasnt found yet
                else:
                    # increment previous tracker and current
                    previousGuest = currentGuest
                    currentGuest = currentGuest.get_next()
        return guestLeaving

    def __repr__(self) -> str:
        hotel_string = self._EMPTY
        if self._size > 0:
            hotel_string = f"\nThere are {self._size} guest(s) in your hotel."
            hotel_string += f"\nThe hotel has a capacity of {self._capacity} rooms."
            hotel_string += f" and is using {self._usage} room(s)."
            hotel_string += f"\nThe load factor is {self._usage/self._capacity:.2f}."
            hotel_string += f" The {self._size} guest(s) are:"
            for room in range(self._capacity):
                if self._hotel[room] is not None:
                    hotel_string += f"\n\tRoom {room:02d}: "
                    guest_in_room = self._hotel[room]
                    while guest_in_room is not None:
                        hotel_string += f"{guest_in_room.get_name()}{self._NEXT_GUEST}"
                        guest_in_room = guest_in_room.get_next()
                    hotel_string += ""
        return hotel_string