#! /usr/bin/env python

from chess.pgn import BaseVisitor
import chess
import re


class EvalsVisitor(BaseVisitor):

    def __init__(self, gm):
        self.game = gm
        self.game.evals = []

    def visit_comment(self, comment):
        if 'eval' in comment:
            evaluation = re.search(r'\[%eval ([^\]]+)', comment).group(1)
        else:
            evaluation = ''
        self.game.evals.append(evaluation)


class ClocksVisitor(BaseVisitor):

    def __init__(self, gm):
        self.game = gm
        self.game.clocks = []

    def visit_comment(self, comment):
        if 'clk' in comment:
            clock_time = re.search(r'\[%clk ([^\]]+)', comment).group(1)
        else:
            clock_time = ''
        self.game.clocks.append(clock_time)


class QueenExchangeVisitor(BaseVisitor):

    def __init__(self, gm):
        self.game = gm

    def begin_game(self):
        self.move_counter = 0
        self.captured_at = 0
        self.game.queen_exchange = False

    def visit_move(self, board, move):
        self.move_counter += 1
        dest = board.piece_at(move.to_square)
        if dest is not None and dest.piece_type == chess.QUEEN:
            if self.captured_at == self.move_counter - 1:
                self.game.queen_exchange = True
            self.captured_at = self.move_counter


class CastlingVisitor(BaseVisitor):

    def __init__(self, gm):
        self.game = gm

    def begin_game(self):
        self.game.castling = {'black': None,
                              'white': None,
                              }

    def visit_move(self, board, move):
        from_sq = board.piece_at(move.from_square)
        if from_sq is not None and from_sq.piece_type == chess.KING:
            if move.to_square == chess.G8:
                self.game.castling['black'] = 'kingside'
            elif move.to_square == chess.G1:
                self.game.castling['white'] = 'kingside'
            elif move.to_square == chess.C8:
                self.game.castling['black'] = 'queenside'
            elif move.to_square == chess.C1:
                self.game.castling['white'] = 'queenside'