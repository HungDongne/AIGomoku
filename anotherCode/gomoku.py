import math
import time
from AI import *
import utils as utils 


def ai_move(ai):
    start_time = time.time()
    ai.alphaBetaPruning(ai.depth, ai.boardValue, ai.nextBound, -math.inf, math.inf, True)
    end_time = time.time()
    print('Finished ab prune in: ', end_time - start_time)
    
    if ai.isValid(ai.currentI, ai.currentJ):
        move_i, move_j = ai.currentI, ai.currentJ
        print(move_i, move_j)
        ai.updateBound(move_i, move_j, ai.nextBound)
        
    else:
        print('Error: i and j not valid. Given: ', ai.currentI, ai.currentJ)
        ai.updateBound(ai.currentI, ai.currentJ, ai.nextBound)
        bound_sorted = sorted(ai.nextBound.items(), key=lambda el: el[1], reverse=True)
        # print(bound_sorted)
        if bound_sorted == []:
            return (-1, -1)
        pos = bound_sorted[0][0]
        move_i = pos[0]
        move_j = pos[1]
        ai.currentI, ai.currentJ = move_i, move_j
        
        print(move_i, move_j)
    
    return move_i, move_j


