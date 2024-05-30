import random
import uuid
from AI import *
##### For managing the interface #####

MARGIN = 23

#### Pattern scores ####
def create_pattern_dict():
    x = -1
    patternDict = {}
    while (x < 2):
        y = -x
        # long_5
        patternDict[(x, x, x, x, x)] = 10000000 * x

        patternDict[(0, y, y, y, x)] = 200000 * x
        patternDict[(x, y, y, y, 0)] = 200000 * x
        patternDict[(x, y, y, y, y, x)] = 300000 * x
        # live_4
        patternDict[(0, x, x, x, x, 0)] = 250000 * x
        patternDict[(0, x, x, x, 0, x, 0)] = 100000 * x
        patternDict[(0, x, 0, x, x, x, 0)] = 100000 * x
        patternDict[(0, x, x, 0, x, x, 0)] = 100000 * x
        # go_4
        patternDict[(0, x, x, x, x, y)] = 10000 * x
        patternDict[(y, x, x, x, x, 0)] = 10000 * x
        # dead_4
        patternDict[(y, x, x, x, x, y)] = -10 * x
        # live_3
        patternDict[(0, x, x, x, 0)] = 1000 * x
        patternDict[(0, x, 0, x, x, 0)] = 1000 * x
        patternDict[(0, x, x, 0, x, 0)] = 1000 * x
        # sleep_3
        patternDict[(0, 0, x, x, x, y)] = 100 * x
        patternDict[(y, x, x, x, 0, 0)] = 100 * x
        patternDict[(0, x, 0, x, x, y)] = 100 * x
        patternDict[(y, x, x, 0, x, 0)] = 100 * x
        patternDict[(0, x, x, 0, x, y)] = 100 * x
        patternDict[(y, x, 0, x, x, 0)] = 100 * x
        patternDict[(x, 0, 0, x, x)] = 100 * x
        patternDict[(x, x, 0, 0, x)] = 100 * x
        patternDict[(x, 0, x, 0, x)] = 100 * x
        patternDict[(y, 0, x, x, x, 0, y)] = 100 * x
        # dead_3
        patternDict[(y, x, x, x, y)] = -10 * x
        # live_2
        patternDict[(0, 0, x, x, 0)] = 100 * x
        patternDict[(0, x, x, 0, 0)] = 100 * x
        patternDict[(0, x, 0, x, 0)] = 100 * x
        patternDict[(0, x, 0, 0, x, 0)] = 100 * x
        # sleep_2
        patternDict[(0, 0, 0, x, x, y)] = 10 * x
        patternDict[(y, x, x, 0, 0, 0)] = 10 * x
        patternDict[(0, 0, x, 0, x, y)] = 10 * x
        patternDict[(y, x, 0, x, 0, 0)] = 10 * x
        patternDict[(0, x, 0, 0, x, y)] = 10 * x
        patternDict[(y, x, 0, 0, x, 0)] = 10 * x
        patternDict[(x, 0, 0, 0, x)] = 10 * x
        patternDict[(y, 0, x, 0, x, 0, y)] = 10 * x
        patternDict[(y, 0, x, x, 0, 0, y)] = 10 * x
        patternDict[(y, 0, 0, x, x, 0, y)] = 10 * x
        # dead_2
        patternDict[(y, x, x, y)] = -10 * x
        x += 2
    return patternDict



##### Zobrist Hashing #####
def init_zobrist(size):
    zTable = [[[uuid.uuid4().int  for _ in range(2)] \
                        for j in range(size)] for i in range(size)] #changed to 32 from 64
    return zTable

def update_TTable(table, hash, score, depth):
    table[hash] = [score, depth]
