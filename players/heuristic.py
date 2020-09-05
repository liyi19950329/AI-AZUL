from advance_model import *
from utils import *
import copy
import numpy as np

class myPlayer(AdvancePlayer):

    def __init__(self,_id):
        super().__init__(_id)

    def StartRound(self,game_state):
        return None

    def SelectMove(self, moves, game_state):
       
        best_score = float('-inf')
        best_move = None

        for mid, fid, tgrab in moves:
            
            move = (mid, fid, tgrab)

            game_state_copy = copy.deepcopy(game_state)

            game_state_copy.ExecuteMove(self.id, move)
            game_state_copy.ExecuteEndOfRound()
            
            score = self.GetScore(game_state_copy)
            if tgrab.num_to_floor_line >= 3:
                score -= tgrab.num_to_floor_line
            
            if score >= best_score:
                best_move = move
                best_score = score

        return best_move
   

    def GetScore(self, game_state):

        score = 0
        plr_state = game_state.players[self.id]
        opp_state = game_state.players[1 - self.id]

        
        # calculate the current score difference between player and opponent
        score = score + plr_state.score - opp_state.score

        # reward for getting end of the game
        if (plr_state.GetCompletedRows()>0) or (opp_state.GetCompletedRows()>0):
            score = 1000*score

        # small reward for go first in next round
        if game_state.first_player == self.id:
            score += 2000

        # penalty for player carrying unfinished lines
        # reward for opponent carrying unfinished lines
        if not game_state.TilesRemaining():
            plr_count = 0
            opp_count = 0

            for i in range(plr_state.GRID_SIZE):
                if plr_state.lines_number[i] != i+1:
                    plr_count += 1
                if opp_state.lines_number[i] != i+1:
                    opp_count += 1

            score = score - (plr_count*plr_count) + (opp_count*opp_count)

        # reward for player's progress towards column bonuses, and penalty for opponent
        for col in range(plr_state.GRID_SIZE):
            plr_progress = 0
            opp_progress = 0

            for row in range(plr_state.GRID_SIZE):
                if plr_state.grid_state[row][col] == 1:
                    plr_progress += (row+1)*(row+1)
                if opp_state.grid_state[row][col] == 1:
                    opp_progress += (row+1)*(row+1)

            score = score + (7*plr_progress) - (7*opp_progress) 

        # reward for player's progress towards color bonuses, and penalty for opponent
        for tile in Tile:
            plr_progress = 0
            opp_progress = 0

            for row in range(plr_state.GRID_SIZE):
                plr_col = plr_state.grid_scheme[row][tile].astype(int)
                if plr_state.grid_state[row][plr_col] == 1:
                    plr_progress += (row+1)*(row+1)
                opp_col = opp_state.grid_scheme[row][tile].astype(int)
                if opp_state.grid_state[row][opp_col] == 1:
                    opp_progress += (row+1)*(row+1)
            
            score = score + (10*plr_progress) - (10*opp_progress)
        
        return score