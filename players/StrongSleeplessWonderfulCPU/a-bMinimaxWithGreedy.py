# This file will be used in the competition
# Please make sure the following functions are well defined

from advance_model import *
from model import *
from utils import *
import numpy as np


# hao version

class myPlayer(AdvancePlayer):

    # initialize
    # The following function should not be changed at all
    def __init__(self, _id):
        super().__init__(_id)
        self.bestbestMove = None
        self.table = {}

    # Each player is given 5 seconds when a new round started
    # If exceeds 5 seconds, all your code will be terminated and
    # you will receive a timeout warning

    def StartRound(self, game_state):
        return None

    def getScoreB(self, move, game, playerId):
        tg = move[2]
        Score = 0
        if tg.num_to_floor_line <= 2:
            Score -= tg.num_to_floor_line
        else:
            Score -= ((tg.num_to_floor_line - 2) * 2 + 2)

        Score += tg.num_to_pattern_line * 0.2

        plystate = game.players[playerId]

        if tg.pattern_line_dest > -1 and tg.pattern_line_dest + 1 == plystate.lines_number[
            tg.pattern_line_dest] + tg.num_to_pattern_line:
            Score += 2

        return Score

    def getScore(self, move, game_state, playerID):
        score = 0
        tg = move[2]
        if tg.num_to_floor_line <= 2:
            score = score - tg.num_to_floor_line
        else:
            score = score - (tg.num_to_floor_line - 2) * 2 - 2
        score = score + tg.num_to_pattern_line * 0.3
        player = game_state.players[playerID]
        line_dest = tg.pattern_line_dest
        # 完成一行加分
        if line_dest > -1 and line_dest + 1 == player.lines_number[line_dest] + tg.num_to_pattern_line:
            score = score + line_dest

        else:
            # 新开一行扣分
            if tg.num_to_pattern_line == player.lines_number[line_dest]:
                score = score - 0.5

        # 帮助完成尚未完成行reward

        if tg.num_to_pattern_line < player.lines_number[line_dest]:
            originNum = player.lines_number[line_dest] - tg.num_to_pattern_line
            score += line_dest * (4 - originNum) * 0.7

        return score

    def alphaBetaMINIMAX(self, gameState, depth, playerId, a, b):
        alpha = a
        beta = b
        gs_copy = copy.deepcopy(gameState)
        remain = gameState.TilesRemaining()
        if depth == 0 or (not remain):
            gs_copy.players[self.id].ScoreRound()
            return gs_copy.players[self.id].score

        if playerId == self.id:
            bestvalue = -1000
            playerState = copy.deepcopy(gameState.players[playerId])
            moves = playerState.GetAvailableMoves(gs_copy)
            for move in moves:
                if self.getScore(move, gameState, playerId) > 1:
                    moveState = copy.deepcopy(gameState)
                    moveState.ExecuteMove(playerId, move)
                    recentValue = self.alphaBetaMINIMAX(moveState, depth - 1, 1 - playerId, alpha, beta)
                    if recentValue > bestvalue:
                        bestvalue = recentValue
                    # alpha-beta prune
                    if bestvalue > alpha:
                        alpha = bestvalue
                    if alpha >= beta:
                        return bestvalue


        else:
            bestvalue = 1000
            playerState = copy.deepcopy(gameState.players[playerId])
            moves = playerState.GetAvailableMoves(gs_copy)
            for move in moves:
                if self.getScore(move, gameState, playerId) > 1:
                    moveState = copy.deepcopy(gameState)
                    moveState.ExecuteMove(playerId, move)
                    recentValue = self.alphaBetaMINIMAX(moveState, depth - 1, 1 - playerId, alpha, beta)
                    if recentValue < bestvalue:
                        bestvalue = recentValue
                    if bestvalue < beta:
                        beta = bestvalue
                    if beta <= alpha:
                        return bestvalue

        return bestvalue

    def SelectMove(self, moves, game_state):
        # Select move that involves placing the most number of tiles
        # in a pattern line. Tie break on number placed in floor line.

        bestscore = -1000
        best_move = None
        if len(moves) > 50:
            best_score = -1000
            for move in moves:

                myScore = self.getScoreB(move, game_state, self.id)
                gs_copy = copy.deepcopy(game_state)
                gs_copy.ExecuteMove(self.id, move)
                opponentState = gs_copy.players[1 - self.id]
                newmoves = opponentState.GetAvailableMoves(gs_copy)
                oppScore = -1000
                for newmove in newmoves:

                    Score = self.getScoreB(newmove, gs_copy, 1 - self.id)
                    if Score > oppScore:
                        oppScore = Score

                if myScore - oppScore > best_score:
                    best_move = move
                    best_score = myScore - oppScore
        else:

            for move in moves:
                moveState = copy.deepcopy(game_state)
                moveState.ExecuteMove(self.id, move)
                recentscore = self.alphaBetaMINIMAX(moveState, 1, 1 - self.id, -1000, 1000)
                if recentscore > bestscore:
                    bestscore = recentscore
                    best_move = move

        return best_move
