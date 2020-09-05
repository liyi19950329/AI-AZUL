# This is just a copy of naive player for submisstion testing
# Try submission-contest
from advance_model import *
from utils import *

class myPlayer(AdvancePlayer):
    def __init__(self, _id):
        super().__init__(_id)

    def SelectMove(self, moves, game_state):
        # A* : f(s) = g(s) + h(s)
        # g(s) = ps.ScoreRound()
        # h(s) = (bonus = ps.EndOfGameScore())
        score = 0
        best_move = None

        for move in moves:
            game_state_copy = copy.deepcopy(game_state)
            game_state_copy.ExecuteMove(self.id, move)
            game_state_copy.ExecuteEndOfRound()
            plr_state = game_state_copy.players[self.id]
            plr_state.EndOfGameScore()
            if plr_state.score >= score:
                best_move = move
                score = plr_state.score

        return best_move

    # def SelectMove(self, moves, game_state):
    #
    #     score = 0
    #     best_move = None
    #
    #     for move in moves:
    #         game_state_copy = copy.deepcopy(game_state)
    #         game_state_copy.ExecuteMove(self.id, move)
    #         game_state_copy.ExecuteEndOfRound()
    #         plr_state = game_state_copy.players[self.id]
    #         # plr_state.ScoreRound()
    #         # bonus = plr_state.EndOfGameScore()
    #         if plr_state.score >= score:
    #             best_move = move
    #             score = plr_state.score
    #
    #     return best_move
