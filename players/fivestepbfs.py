# This is just a copy of naive player for submisstion testing
# Try submission-contest
from advance_model import *
from utils import *

class myPlayer(AdvancePlayer):
    def __init__(self, _id):
        super().__init__(_id)

    # def evaluation(self, move, plr_state, playerID):
    #     score = 0
    #     bonus = 0
    #     mid, fid, tgrab = move
    #
    #     if tgrab.num_to_floor_line <= 2:
    #         score = score - tgrab.num_to_floor_line
    #     else:
    #         score = score - (tgrab.num_to_floor_line - 2) * 2 - 2
    #
    #     i = tgrab.pattern_line_dest
    #     # col = int(plr_state.grid_scheme[i][tgrab.tile_type])
    #     # if plr_state.grid_state[i][col] == 0 and i + 1 == plr_state.lines_number[i] + tgrab.num_to_pattern_line:
    #     #     score = 10
    #
    #     if i + 1 == plr_state.lines_number[i] + tgrab.num_to_pattern_line:
    #         col = int(plr_state.grid_scheme[i][tgrab.tile_type])
    #
    #         above = 0
    #         for j in range(col - 1, -1, -1):
    #             val = plr_state.grid_state[i][j]
    #             above += val
    #             if val == 0:
    #                 break
    #         below = 0
    #         for j in range(col + 1, 5, 1):
    #             val = plr_state.grid_state[i][j]
    #             below += val
    #             if val == 0:
    #                 break
    #         left = 0
    #         for j in range(i - 1, -1, -1):
    #             val = plr_state.grid_state[j][col]
    #             left += val
    #             if val == 0:
    #                 break
    #         right = 0
    #         for j in range(i + 1, 5, 1):
    #             val = plr_state.grid_state[j][col]
    #             right += val
    #             if val == 0:
    #                 break
    #
    #         if above > 0 or below > 0:
    #             score += (1 + above + below)
    #         if left > 0 or right > 0:
    #             score += (1 + left + right)
    #         if above == 0 and below == 0 and left == 0 and right == 0:
    #             score += 1
    #
    #         plr_state.grid_state[i][col] = 1
    #
    #         # grid_state_self = plr_state.grid_state
    #
    #         completed_rows = 0
    #         for k in range(5):
    #             allin = True
    #             for j in range(5):
    #                 if plr_state.grid_state[k][j] == 0:
    #                     allin = False
    #                     break
    #             if allin:
    #                 completed_rows += 1
    #         #
    #         completed_cols = 0
    #         for k in range(5):
    #             allin = True
    #             for j in range(5):
    #                 if plr_state.grid_state[j][k] == 0:
    #                     allin = False
    #                     break
    #             if allin:
    #                 completed_cols += 1
    #         #
    #         completed_sets = 0
    #         for tile in Tile:
    #             if plr_state.number_of[tile] == 5:
    #                 completed_sets += 1
    #         #
    #         bonus = (completed_rows * 2) + (completed_cols * 7) + (completed_sets * 10)
    #
    #
    #
    #     # if tgrab.num_to_floor_line > 0:
    #     #     ttf = []
    #     #     for i in range(tgrab.num_to_floor_line):
    #     #         ttf.append(tgrab.tile_type)
    #     #     plr_state.AddToFloor(ttf)
    #
    #     # if tgrab.num_to_pattern_line > 0:
    #     #     plr_state.lines_number[tgrab.pattern_line_dest] += tgrab.num_to_pattern_line
    #     #     plr_state.lines_tile[tgrab.pattern_line_dest] = tgrab.tile_type
    #
    #         # plr_state.AddToPatternLine(tgrab.pattern_line_dest,
    #         #                            tgrab.num_to_pattern_line, tgrab.tile_type)
    #
    #     # plr_state.ScoreRound()
    #     # plr_state.EndOfGameScore()
    #     return plr_state.score + score + bonus

    def evaluation(self, move, player, playerID):
        score = 0
        mid, fid, tgrab = move
        if tgrab.num_to_floor_line <= 2:
            score = score - tgrab.num_to_floor_line
        else:
            score = score - (tgrab.num_to_floor_line - 2) * 2 - 2

        score = score + tgrab.num_to_pattern_line * 0.2

        # player = game_state.players[playerID]

        i = tgrab.pattern_line_dest
        if i > -1 and i + 1 == player.lines_number[i] + tgrab.num_to_pattern_line:
            score = score + 2

        return score

    def maxMove(self,game_state,id):
        best_score = -999
        best_move = None

        plr_state = game_state.players[id]
        moves = plr_state.GetAvailableMoves(game_state)

        for move in moves:
            my_score = self.evaluation(move, plr_state,id)
            if my_score >= best_score:
                best_move = move
                best_score = my_score
        game_state.ExecuteMove(id, best_move)
        return best_move, game_state, best_score

    def SelectMove(self, moves, game_state):
        best_move = None
        best_score = -999

        for move in moves:

            next_state = copy.deepcopy(game_state)

            next_state.ExecuteMove(self.id, move)

            plr_state_f = next_state.players[self.id]

            my_score = self.evaluation(move, plr_state_f, self.id)

            if not next_state.TilesRemaining():
                best_move = move
                break

            # opp = next_state.players[1 - self.id]
            #
            # opp_moves = opp.GetAvailableMoves(next_state)
            #
            # opp_moves_copy = copy.deepcopy(opp_moves)

            move_opp,nn_state,score_opp = self.maxMove(next_state,1 - self.id)

            if not nn_state.TilesRemaining():
                if my_score - score_opp > best_score:
                    best_move = move
                    best_score = my_score - score_opp
                continue

            # self_plr = nn_state.players[self.id]
            # self_moves = self_plr.GetAvailableMoves(nn_state)
            # self_moves_copy = copy.deepcopy(self_moves)

            move_self, nnn_state, score_self = self.maxMove(nn_state, self.id)

            if not nnn_state.TilesRemaining():
                if score_self + my_score - score_opp > best_score:
                    best_move = move
                    best_score = score_self + my_score - score_opp
                continue

            # opp = nnn_state.players[1 - self.id]
            #
            # opp_moves = opp.GetAvailableMoves(nnn_state)
            #
            # opp_moves_copy = copy.deepcopy(opp_moves)

            move_oppp, nnnn_state, score_oppp = self.maxMove(nnn_state, 1 - self.id)

            if not nnnn_state.TilesRemaining():
                if score_self + my_score - score_opp - score_oppp > best_score:
                    best_move = move
                    best_score = score_self + my_score - score_opp - score_oppp
                continue

            # self_plr = nnnn_state.players[self.id]
            # self_moves = self_plr.GetAvailableMoves(nnnn_state)
            # self_moves_copy = copy.deepcopy(self_moves)

            move_selff, nnnnn_state, score_selff = self.maxMove(nnnn_state, self.id)

            if score_self + my_score + score_selff - score_opp - score_oppp >= best_score:
                best_move = move
                best_score = score_self + my_score + score_selff - score_opp - score_oppp

        return best_move
