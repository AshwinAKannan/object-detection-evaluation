from enum import Enum


class PascalVocSampleClassMapping(Enum):
    
    background = -1
    aeroplane = 0
    bicycle = 1
    bird = 2
    boat = 3
    bottle = 4
    bus = 5
    car = 6
    cat = 7
    chair = 8
    cow = 9
    diningtable = 10
    dog = 11
    horse = 12
    motorbike = 13
    person = 14
    pottedplant = 15
    sheep = 16
    sofa = 17
    train = 18
    tvmonitor = 19
    
    @staticmethod
    def get_class_id(name):
        return PascalVocSampleClassMapping.__members__.get(name.lower()).value
    