# This is just a copy of naive player for submisstion testing
# Try submission-contest
from advance_model import *
from utils import *

class myPlayer(AdvancePlayer):
    def __init__(self, _id):
        super().__init__(_id)

    def evaluation(self, move, game_state, playerID):
        score = 0
        mid, fid, tgrab = move
        if tgrab.num_to_floor_line <= 2:
            score = score - tgrab.num_to_floor_line
        else:
            score = score - (tgrab.num_to_floor_line - 2) * 2 - 2

        score = score + tgrab.num_to_pattern_line * 0.2

        player = game_state.players[playerID]

        i = tgrab.pattern_line_dest
        if i > -1 and i + 1 == player.lines_number[i] + tgrab.num_to_pattern_line:
            score = score + 2

        return score
    def maxMove(self,game_state,moves,id):
        best_score = -999
        best_move = None
        for move in moves:
            my_score = self.evaluation(move, game_state,id)
            if my_score > best_score:
                best_move = move
                best_score = my_score
        game_state.ExecuteMove(id, best_move)
        return best_move, game_state, best_score

    def SelectMove(self, moves, game_state):

        best_move = None
        best_score = -999

        for move in moves:
            my_score = self.evaluation(move, game_state, self.id)

            next_state = copy.deepcopy(game_state)

            next_state.ExecuteMove(self.id, move)

            if not next_state.TilesRemaining():
                best_move = move
                break

            opp = next_state.players[1 - self.id]

            opp_moves = opp.GetAvailableMoves(next_state)

            opp_moves_copy = copy.deepcopy(opp_moves)

            move_opp,nn_state,score_opp = self.maxMove(next_state,opp_moves_copy,1-self.id)

            if not nn_state.TilesRemaining():
                if my_score - score_opp > best_score:
                    best_move = move
                    best_score = my_score - score_opp
                continue

            self_plr = nn_state.players[self.id]
            self_moves = self_plr.GetAvailableMoves(nn_state)
            self_moves_copy = copy.deepcopy(self_moves)

            move_self, nnn_state, score_self = self.maxMove(nn_state, self_moves_copy, self.id)

            if score_self + my_score - score_opp > best_score:
                best_move = move
                best_score = score_self + my_score - score_opp


        return best_move
