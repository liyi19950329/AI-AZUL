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
        self.Q_Table = {}
        self.OneStepValue = {}

    # Each player is given 5 seconds when a new round started
    # If exceeds 5 seconds, all your code will be terminated and 
    # you will receive a timeout warning
    def StartRound(self, game_state):

        gs_copy = copy.deepcopy(game_state)
        self.MCTS(gs_copy, 100, 5)
        return None

    # Each player is given 1 second to select next best move
    # If exceeds 5 seconds, all your code will be terminated, 
    # a random action will be selected, and you will receive 
    # a timeout warning

    def initialQ_Table(self, gameState):
        Q_Table_New = copy.deepcopy(self.Q_Table)


        return Q_Table_New

    def selectOpponentMove(self, moves):
        # Select move that involves placing the most number of tiles
        # in a pattern line. Tie break on number placed in floor line.
        most_to_line = -1
        corr_to_floor = 0

        best_move = None

        for mid, fid, tgrab in moves:
            if most_to_line == -1:
                best_move = (mid, fid, tgrab)
                most_to_line = tgrab.num_to_pattern_line
                corr_to_floor = tgrab.num_to_floor_line
                continue

            if tgrab.num_to_pattern_line > most_to_line:
                best_move = (mid, fid, tgrab)
                most_to_line = tgrab.num_to_pattern_line
                corr_to_floor = tgrab.num_to_floor_line
            elif tgrab.num_to_pattern_line == most_to_line and \
                    tgrab.num_to_floor_line < corr_to_floor:
                best_move = (mid, fid, tgrab)
                most_to_line = tgrab.num_to_pattern_line
                corr_to_floor = tgrab.num_to_floor_line

        return best_move

    def MCTS(self, gameState, times, deep):

        alpha = 0.8  # 学习率
        gamma = 0.5  # 奖励递减率

        arrivedList = []

        for i in range(times):
            curr_state = copy.deepcopy(gameState.players[self.id])
            curr_stateB = copy.deepcopy(gameState.players[0])
            curr_gameState = copy.deepcopy(gameState)
            moves = copy.deepcopy(curr_state.GetAvailableMoves(curr_gameState))

            # 生成一个简便状态点存储Q值（只考虑playerstate，不管gamestate），应该可以改进
            curr_stateMark = PlayerToString(self.id, curr_state)
            expandList = []
            expandMoveList = []
            finishedFlag = False
            reward = 0
            cost = 0

            for j in range(deep):
                if moves and (j < deep - 1):

                    expandList.append(curr_stateMark)
                    moves = copy.deepcopy(curr_state.GetAvailableMoves(curr_gameState))
                    if len(moves) >= 1:
                        # 根据权重随机选择点
                        maxValue, bestAction = self.randomAction(moves, curr_stateMark, curr_gameState)
                        # update gamestate, playerstate
                        next_gameState = copy.deepcopy(curr_gameState)
                        next_gameState.ExecuteMove(self.id, bestAction)
                        next_state = copy.deepcopy(next_gameState.players[self.id])
                        movestr = MoveToString(self.id, bestAction)

                        # 生成一个简便状态点存储Q值（只考虑playerstate，不管gamestate），应该可以改进
                        next_stateMark = PlayerToString(self.id, next_state)
                        expandMoveList.append(movestr)

                        tg = copy.deepcopy(bestAction[2])
                        line_dest = tg.pattern_line_dest
                        completeReward = 0
                        central_reward = 0
                        helpCompleteReward = 0
                        moveFrom = bestAction[0]
                        continousReward = 0
                        if moveFrom == Move.TAKE_FROM_CENTRE:
                            central_reward = 0.5

                        score_inc = 0

                        if tg.num_to_floor_line == 0:
                            lineNum = line_dest + 1
                            comboNumber = tg.number - 1
                            freeBlock = line_dest + 1 - next_state.lines_number[line_dest]
                            # 完成某一行加分，越下面加越多
                            if freeBlock == 0:
                                completeReward = (lineNum - 1) * 1.2

                            totalNum = tg.number
                            num_to_pattern_line = tg.num_to_pattern_line
                            overFlowNum = num_to_pattern_line - totalNum
                            num_to_floor_line = 0
                            # 新作一行的代价
                            if num_to_pattern_line == next_state.lines_number[line_dest]:
                                newLine_cost = -0.6 * line_dest * (lineNum - num_to_pattern_line - comboNumber)
                            else:
                                newLine_cost = 0

                            # 帮助完成尚未完成行reward

                            if num_to_pattern_line < next_state.lines_number[line_dest]:
                                originNum = next_state.lines_number[line_dest] - num_to_pattern_line
                                helpCompleteReward = lineNum * (4 - originNum) * 0.7
                        else:
                            lineNum = 1
                            comboNumber = 0
                            freeBlock = 0
                            overFlowNum = 0
                            num_to_pattern_line = 0
                            continousNum = 0
                            num_to_floor_line = tg.num_to_floor_line
                            newLine_cost = 0

                        comboReward = 1
                        lineReward = 1
                        score_change_reward = 1
                        continousReward = 0

                        # 拿完后空格的代价
                        freeCost = -0.5
                        # 拿太多凑一行的代价
                        overFlowCost = -1
                        # 直接拿到扣分的cost
                        directFloorCost = -1.8

                        reward += comboNumber * comboReward * (lineNum - 2) + completeReward + lineReward * ((num_to_pattern_line / lineNum) - 0.5) + helpCompleteReward + central_reward
                        # 后面行，每次放的越多，reward越高
                        # num_to_pattern / lineNum表示越下面行放越少加分越少
                        # Cost 计算，freeBlock为空格，空的越多越不好

                        cost += freeCost * freeBlock + overFlowCost * overFlowNum + num_to_floor_line * directFloorCost + newLine_cost

                        next_stateMarkB = PlayerToString(1-self.id, curr_stateB)
                        movesB = copy.deepcopy(curr_stateB.GetAvailableMoves(next_gameState))
                        if movesB:
                            opponentMove = self.selectOpponentMove(movesB)
                            # opponentMove = self.selectAdvance(movesB, next_gameState)
                            next_gameState.ExecuteMove(1-self.id, opponentMove)
                            next_stateB = next_gameState.players[1-self.id]
                            next_stateMarkB = PlayerToString(1-self.id, next_stateB)

                        moves = copy.deepcopy(next_state.GetAvailableMoves(next_gameState))

                        # 更新当前状态
                        curr_stateB = copy.deepcopy(next_gameState.players[0])
                        curr_state = copy.deepcopy(next_state)
                        curr_stateMark = PlayerToString(self.id, curr_state)
                        curr_gameState = copy.deepcopy(next_gameState)
                        full = True


                else:
                    # 计算最后的值
                    # 选择一个扣分最多的
                    curr_stateMark = PlayerToString(self.id, curr_state)
                    origin_Score = curr_state.score
                    origin_ScoreB = curr_stateB.score

                    curr_state.ScoreRound()
                    curr_stateB.ScoreRound()
                    curr_state.EndOfGameScore()
                    curr_stateB.EndOfGameScore()

                    # Value
                    score_change = curr_state.score - origin_Score
                    score_changeB = curr_stateB.score - origin_ScoreB
                    # (reward + cost)是 policy影响，即hardcode


                    value = (score_change - score_changeB) * 5 + (reward + cost) * 0.3

                    deepLen = len(expandMoveList)
                    # BackPropogation
                    gammaRate = 1
                    for backIndex in range(deepLen):
                        gammaRate *= gamma
                        executeMove = expandMoveList[deepLen - 1 - backIndex]
                        executeState = expandList[deepLen - 1 - backIndex]
                        if executeState in self.Q_Table:
                            move_Table = copy.deepcopy(self.Q_Table.get(executeState))
                            oldValue = 0
                            if executeMove in move_Table:
                                oldValue = move_Table.get(executeMove)
                            newValue = (oldValue + value) / 2
                            move_Table.update({executeMove: newValue})
                            self.Q_Table.update({executeState: move_Table})
                        else:
                            move_Table = {}
                            newValue = value
                            move_Table.update({executeMove: newValue})
                            self.Q_Table.update({executeState: move_Table})

        return None

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

    def randomAction(self, moves, curr_stateMark, curr_gameState):
        moveOption = copy.deepcopy(moves)
        curr_state = copy.deepcopy(curr_gameState.players[self.id])
        score_state = copy.deepcopy(curr_state)
        continuousReward = 0

        legalQ = []
        i = -1
        reward = 0
        cost = 0

        if curr_stateMark in self.Q_Table:
            currentQ = self.Q_Table.get(curr_stateMark)
            for move in moveOption:
                i += 1
                movestr = MoveToString(self.id, move)
                if movestr in currentQ:
                    legalQ.append(currentQ.get(movestr))
                else:
                    legalQ.append(0)

            maxValue = max(legalQ)

            bestActions = [move for move, value in zip(moveOption, legalQ) if value == maxValue]

            bestAction = random.choice(bestActions)

            # 一定几率选择最优动作以外的动作
            chance = random.randint(1, 10)
            if chance > 7 and len(moves) >= 2:
                tmpActions = [move for move, value in zip(moveOption, legalQ)]
                bestAction = random.choice(tmpActions)
                a = -1
                for action in tmpActions:
                    a += 1
                    if action == bestAction:
                        break
                maxValue = legalQ[a]

        elif curr_stateMark not in self.Q_Table:
            origin_score = curr_state.score
            bestActions = [move for move in moveOption]
            bestAction = random.choice(bestActions)
            gamestate = copy.deepcopy(curr_gameState)
            gamestate.ExecuteMove(self.id, bestAction)
            score_state = copy.deepcopy(curr_gameState.players[self.id])
            maxValue = 0

        return maxValue, bestAction

    def SelectMove(self, moves, game_state):
        # Select move that involves placing the most number of tiles
        # in a pattern line. Tie break on number placed in floor line.
        most_to_line = -1
        corr_to_floor = 0
        most_score = 0




        best_move = None

        maxValue = -1000

        if len(moves)>100:
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

        else:
            curr_state = PlayerToString(self.id, game_state.players[self.id])
            self.MCTS(game_state, 50, 2)
            move_Table = copy.deepcopy(self.Q_Table.get(curr_state))

            for move in moves:
                movestr = MoveToString(self.id, move)
                if movestr in move_Table:
                    value = move_Table.get(movestr)
                    if value > maxValue:
                        best_move = move
                        maxValue = value
            if not best_move:
                for mid, fid, tgrab in moves:
                    if most_to_line == -1:
                        best_move = (mid, fid, tgrab)
                        most_to_line = tgrab.num_to_pattern_line
                        corr_to_floor = tgrab.num_to_floor_line
                        continue

                    if tgrab.num_to_pattern_line > most_to_line:
                        best_move = (mid, fid, tgrab)
                        most_to_line = tgrab.num_to_pattern_line
                        corr_to_floor = tgrab.num_to_floor_line
                    elif tgrab.num_to_pattern_line == most_to_line and \
                            tgrab.num_to_floor_line < corr_to_floor:
                        best_move = (mid, fid, tgrab)
                        most_to_line = tgrab.num_to_pattern_line
                        corr_to_floor = tgrab.num_to_floor_line
        # if not best_move:
        #    best_move = random.choice(moves)
        return best_move
