from advance_model import *
from utils import *


class myPlayer(AdvancePlayer):
    def __init__(self, _id):
        super().__init__(_id)

    def getScore(self, move, game, playerId):
        tg = move[2]
        Score = 0
        if tg.num_to_floor_line <= 2:
            Score -= tg.num_to_floor_line
        else:
            Score -= ((tg.num_to_floor_line - 2) * 2 + 2)

        Score += tg.num_to_pattern_line * 0.2

        plystate = game.players[playerId]

        if tg.pattern_line_dest > -1 and tg.pattern_line_dest + 1 == plystate.lines_number[tg.pattern_line_dest] + tg.num_to_pattern_line:
            Score += 2

        return Score

    def SelectMove(self, moves, game_state):
        # Select move that involves placing the most number of tiles
        # in a pattern line. Tie break on number placed in floor line.
        most_to_line = -1
        corr_to_floor = 0

        best_move = None
        best_score = -1000

        for move in moves:

            myScore = self.getScore(move, game_state, self.id)
            gs_copy = copy.deepcopy(game_state)
            gs_copy.ExecuteMove(self.id, move)
            opponentState = gs_copy.players[1 - self.id]
            newmoves = opponentState.GetAvailableMoves(gs_copy)
            oppScore = -1000
            for newmove in newmoves:

                Score = self.getScore(newmove, gs_copy, 1 - self.id)
                if Score > oppScore:
                    oppScore = Score

            if myScore - oppScore > best_score:
                best_move = move
                best_score = myScore - oppScore

        return best_move
