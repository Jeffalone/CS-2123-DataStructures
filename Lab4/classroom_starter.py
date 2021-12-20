# implement a greedy algorithm to solve classroom scheduling problems
# priority queues are required

import datetime
from heapq import heappush, heappop


def scheduleRooms(rooms, cls):
    """
    Input: rooms - list of available rooms
           cls   - dictionary mapping class names to pair of (start,end) times
    Output: Return a dictionary mapping the room name to a list of 
    non-conflicting scheduled classes. 
    If there are not enough rooms to hold the classes, return 'Not enough rooms'.
    """
    rmassign = {}  # set holding room assignments

    classStartQ = []  # will store in heap as (start time, class label)
    roomEndQ = []  # will store in queue as (end time, room number)

    for x in cls.keys():
        heappush(classStartQ, (cls[x][0], x))

    for room in rooms:
        rmassign[room] = []  # initialize each room schedule to be empty

    roomsInUse = 0  # initialize amount of open rooms
    heappush(roomEndQ, (datetime.time(0), rooms[
        roomsInUse]))  # open first room with minimum time so it will be garunteed to assigned to first class.
    roomsInUse += 1

    while classStartQ:
        startTime, className = heappop(classStartQ)
        endTime, roomName = heappop(roomEndQ)

        if endTime <= startTime:
            rmassign[roomName].append(className)  # assigns room
            heappush(roomEndQ, (cls[className][1], roomName))  # updates room's end time

        elif roomsInUse < len(rooms):  # there are still rooms that need to be opened
            heappush(classStartQ, (startTime, className))  # return class and failed room to heap
            heappush(roomEndQ, (endTime, roomName))
            heappush(roomEndQ, (datetime.time(0), rooms[
                roomsInUse])) # open new room so it will be used for the next class that was just put back into the heap
            roomsInUse += 1  # increment the amount of rooms that have been opened
        else:
            return "Not Enough Rooms"  # exceeded the number of rooms allowed
    return rmassign


if __name__ == "__main__":
    cl1 = {"a": (datetime.time(9), datetime.time(10, 30)),
           "b": (datetime.time(9), datetime.time(12, 30)),
           "c": (datetime.time(9), datetime.time(10, 30)),
           "d": (datetime.time(11), datetime.time(12, 30)),
           "e": (datetime.time(11), datetime.time(14)),
           "f": (datetime.time(13), datetime.time(14, 30)),
           "g": (datetime.time(13), datetime.time(14, 30)),
           "h": (datetime.time(14), datetime.time(16, 30)),
           "i": (datetime.time(15), datetime.time(16, 30)),
           "j": (datetime.time(15), datetime.time(16, 30))}
    rm1 = [1, 2, 3]
    print(cl1)
    print(scheduleRooms(rm1, cl1))
    print(scheduleRooms([1, 2], cl1))
    ensrooms = ['KEH U1', 'KEH M1', 'KEH M2', 'KEH M3', 'KEH U2', 'KEH U3', 'KEH U4', 'KEH M4', 'KEH U8', 'KEH U9']
    csclasses = {'CS 1043': (datetime.time(9, 30), datetime.time(11)),
                 'CS 2003': (datetime.time(10, 30), datetime.time(12)),
                 'CS 2123': (datetime.time(11, 15), datetime.time(12, 45)),
                 'CS 3003': (datetime.time(8, 15), datetime.time(11, 30)),
                 'CS 3353': (datetime.time(11), datetime.time(12)),
                 'CS 4013': (datetime.time(13), datetime.time(14, 45)),
                 'CS 4063': (datetime.time(12, 30), datetime.time(14, 30)),
                 'CS 4123': (datetime.time(14), datetime.time(15)),
                 'CS 4163': (datetime.time(14), datetime.time(16, 30)),
                 'CS 4253': (datetime.time(12), datetime.time(16)),
                 }
    print(csclasses)
    print(scheduleRooms(ensrooms, csclasses))
    print(scheduleRooms(ensrooms[:4], csclasses))
