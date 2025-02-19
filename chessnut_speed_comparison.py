# This script compares the time it takes to generate the moves for a given list of FEN positions using Chessnut and Chessir.
# Note that it is necessary to install Chessnut for this script to work.

from Chessnut import Game as ChessnutGame
from src.Chessir.game import Game
import time

def time_moves(fen_list):

    runs = 10
    chessnut_time = 0
    chessir_time = 0

    for run in range(runs):
        if run % 2 == 0: chessnut_first = True
        else: chessnut_first = False    
        for fen in fen_list:
            if chessnut_first:
                start_time = time.time()
                game = ChessnutGame(fen)
                moves = game.get_moves()
                end_time = time.time()
                chessnut_time += end_time - start_time

                start_time = time.time()
                game = Game(fen)
                moves = game.get_moves()
                end_time = time.time()
                chessir_time += end_time - start_time
            else:
                start_time = time.time()
                game = Game(fen)
                moves = game.get_moves()
                end_time = time.time()
                chessir_time += end_time - start_time

                start_time = time.time()
                game = ChessnutGame(fen)
                moves = game.get_moves()
                end_time = time.time()
                chessnut_time += end_time - start_time

    print('Chessnut time:', chessnut_time)
    print('Chessir time:', chessir_time)

test_fens = [
    # Kasparov vs Topalov 1999
    'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
    'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1',
    'rnbqkbnr/ppp1pppp/3p4/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2',
    'rnbqkbnr/ppp1pppp/3p4/8/3PP3/8/PPP2PPP/RNBQKBNR b KQkq - 0 2',
    'rnbqkb1r/ppp1pppp/3p1n2/8/3PP3/8/PPP2PPP/RNBQKBNR w KQkq - 1 3',
    'rnbqkb1r/ppp1pppp/3p1n2/8/3PP3/2N5/PPP2PPP/R1BQKBNR b KQkq - 2 3',
    'rnbqkb1r/ppp1pp1p/3p1np1/8/3PP3/2N5/PPP2PPP/R1BQKBNR w KQkq - 0 4',
    'rnbqkb1r/ppp1pp1p/3p1np1/8/3PP3/2N1B3/PPP2PPP/R2QKBNR b KQkq - 1 4',
    'rnbqk2r/ppp1ppbp/3p1np1/8/3PP3/2N1B3/PPP2PPP/R2QKBNR w KQkq - 2 5',
    'rnbqk2r/ppp1ppbp/3p1np1/8/3PP3/2N1B3/PPPQ1PPP/R3KBNR b KQkq - 3 5',
    'rnbqk2r/pp2ppbp/2pp1np1/8/3PP3/2N1B3/PPPQ1PPP/R3KBNR w KQkq - 0 6',
    'rnbqk2r/pp2ppbp/2pp1np1/8/3PP3/2N1BP2/PPPQ2PP/R3KBNR b KQkq - 0 6',
    'rnbqk2r/p3ppbp/2pp1np1/1p6/3PP3/2N1BP2/PPPQ2PP/R3KBNR w KQkq - 0 7',
    'rnbqk2r/p3ppbp/2pp1np1/1p6/3PP3/2N1BP2/PPPQN1PP/R3KB1R b KQkq - 1 7',
    'r1bqk2r/p2nppbp/2pp1np1/1p6/3PP3/2N1BP2/PPPQN1PP/R3KB1R w KQkq - 2 8',
    'r1bqk2r/p2nppbp/2pp1npB/1p6/3PP3/2N2P2/PPPQN1PP/R3KB1R b KQkq - 3 8',
    'r1bqk2r/p2npp1p/2pp1npb/1p6/3PP3/2N2P2/PPPQN1PP/R3KB1R w KQkq - 0 9',
    'r1bqk2r/p2npp1p/2pp1npQ/1p6/3PP3/2N2P2/PPP1N1PP/R3KB1R b KQkq - 0 9',
    'r2qk2r/pb1npp1p/2pp1npQ/1p6/3PP3/2N2P2/PPP1N1PP/R3KB1R w KQkq - 1 10',
    'r2qk2r/pb1npp1p/2pp1npQ/1p6/3PP3/P1N2P2/1PP1N1PP/R3KB1R b KQkq - 0 10',
    'r2qk2r/pb1n1p1p/2pp1npQ/1p2p3/3PP3/P1N2P2/1PP1N1PP/R3KB1R w KQkq - 0 11',
    'r2qk2r/pb1n1p1p/2pp1npQ/1p2p3/3PP3/P1N2P2/1PP1N1PP/2KR1B1R b kq - 1 11',
    'r3k2r/pb1nqp1p/2pp1npQ/1p2p3/3PP3/P1N2P2/1PP1N1PP/2KR1B1R w kq - 2 12',
    'r3k2r/pb1nqp1p/2pp1npQ/1p2p3/3PP3/P1N2P2/1PP1N1PP/1K1R1B1R b kq - 3 12',
    'r3k2r/1b1nqp1p/p1pp1npQ/1p2p3/3PP3/P1N2P2/1PP1N1PP/1K1R1B1R w kq - 0 13',
    'r3k2r/1b1nqp1p/p1pp1npQ/1p2p3/3PP3/P1N2P2/1PP3PP/1KNR1B1R b kq - 1 13',
    '2kr3r/1b1nqp1p/p1pp1npQ/1p2p3/3PP3/P1N2P2/1PP3PP/1KNR1B1R w - - 2 14',
    '2kr3r/1b1nqp1p/p1pp1npQ/1p2p3/3PP3/PNN2P2/1PP3PP/1K1R1B1R b - - 3 14',
    '2kr3r/1b1nqp1p/p1pp1npQ/1p6/3pP3/PNN2P2/1PP3PP/1K1R1B1R w - - 0 15',
    '2kr3r/1b1nqp1p/p1pp1npQ/1p6/3RP3/PNN2P2/1PP3PP/1K3B1R b - - 0 15',
    '2kr3r/1b1nqp1p/p2p1npQ/1pp5/3RP3/PNN2P2/1PP3PP/1K3B1R w - - 0 16',
    '2kr3r/1b1nqp1p/p2p1npQ/1pp5/4P3/PNN2P2/1PP3PP/1K1R1B1R b - - 1 16',
    '2kr3r/1b2qp1p/pn1p1npQ/1pp5/4P3/PNN2P2/1PP3PP/1K1R1B1R w - - 2 17',
    '2kr3r/1b2qp1p/pn1p1npQ/1pp5/4P3/PNN2PP1/1PP4P/1K1R1B1R b - - 0 17',
    '1k1r3r/1b2qp1p/pn1p1npQ/1pp5/4P3/PNN2PP1/1PP4P/1K1R1B1R w - - 1 18',
    '1k1r3r/1b2qp1p/pn1p1npQ/Npp5/4P3/P1N2PP1/1PP4P/1K1R1B1R b - - 2 18',
    'bk1r3r/4qp1p/pn1p1npQ/Npp5/4P3/P1N2PP1/1PP4P/1K1R1B1R w - - 3 19',
    'bk1r3r/4qp1p/pn1p1npQ/Npp5/4P3/P1N2PPB/1PP4P/1K1R3R b - - 4 19',
    'bk1r3r/4qp1p/pn3npQ/Nppp4/4P3/P1N2PPB/1PP4P/1K1R3R w - - 0 20',
    'bk1r3r/4qp1p/pn3np1/Nppp4/4PQ2/P1N2PPB/1PP4P/1K1R3R b - - 1 20',
    'b2r3r/k3qp1p/pn3np1/Nppp4/4PQ2/P1N2PPB/1PP4P/1K1R3R w - - 2 21',
    'b2r3r/k3qp1p/pn3np1/Nppp4/4PQ2/P1N2PPB/1PP4P/1K1RR3 b - - 3 21',
    'b2r3r/k3qp1p/pn3np1/Npp5/3pPQ2/P1N2PPB/1PP4P/1K1RR3 w - - 0 22',
    'b2r3r/k3qp1p/pn3np1/NppN4/3pPQ2/P4PPB/1PP4P/1K1RR3 b - - 1 22',
    'b2r3r/k3qp1p/p4np1/Nppn4/3pPQ2/P4PPB/1PP4P/1K1RR3 w - - 0 23',
    'b2r3r/k3qp1p/p4np1/NppP4/3p1Q2/P4PPB/1PP4P/1K1RR3 b - - 0 23',
    'b2r3r/k4p1p/p2q1np1/NppP4/3p1Q2/P4PPB/1PP4P/1K1RR3 w - - 1 24',
    'b2r3r/k4p1p/p2q1np1/NppP4/3R1Q2/P4PPB/1PP4P/1K2R3 b - - 0 24',
    'b2r3r/k4p1p/p2q1np1/Np1P4/3p1Q2/P4PPB/1PP4P/1K2R3 w - - 0 25',
    'b2r3r/k3Rp1p/p2q1np1/Np1P4/3p1Q2/P4PPB/1PP4P/1K6 b - - 1 25',
    'b2r3r/4Rp1p/pk1q1np1/Np1P4/3p1Q2/P4PPB/1PP4P/1K6 w - - 2 26',
    'b2r3r/4Rp1p/pk1q1np1/Np1P4/3Q4/P4PPB/1PP4P/1K6 b - - 0 26',
    'b2r3r/4Rp1p/p2q1np1/kp1P4/3Q4/P4PPB/1PP4P/1K6 w - - 0 27',
    'b2r3r/4Rp1p/p2q1np1/kp1P4/1P1Q4/P4PPB/2P4P/1K6 b - - 0 27',
    'b2r3r/4Rp1p/p2q1np1/1p1P4/kP1Q4/P4PPB/2P4P/1K6 w - - 1 28',
    'b2r3r/4Rp1p/p2q1np1/1p1P4/kP6/P1Q2PPB/2P4P/1K6 b - - 2 28',
    'b2r3r/4Rp1p/p4np1/1p1q4/kP6/P1Q2PPB/2P4P/1K6 w - - 0 29',
    'b2r3r/R4p1p/p4np1/1p1q4/kP6/P1Q2PPB/2P4P/1K6 b - - 1 29',
    '3r3r/Rb3p1p/p4np1/1p1q4/kP6/P1Q2PPB/2P4P/1K6 w - - 2 30',
    '3r3r/1R3p1p/p4np1/1p1q4/kP6/P1Q2PPB/2P4P/1K6 b - - 0 30',
    '3r3r/1R3p1p/p4np1/1p6/kPq5/P1Q2PPB/2P4P/1K6 w - - 1 31',
    '3r3r/1R3p1p/p4Qp1/1p6/kPq5/P4PPB/2P4P/1K6 b - - 0 31',
    '3r3r/1R3p1p/p4Qp1/1p6/1Pq5/k4PPB/2P4P/1K6 w - - 0 32',
    '3r3r/1R3p1p/Q5p1/1p6/1Pq5/k4PPB/2P4P/1K6 b - - 0 32',
    '3r3r/1R3p1p/Q5p1/1p6/1kq5/5PPB/2P4P/1K6 w - - 0 33',
    '3r3r/1R3p1p/Q5p1/1p6/1kq5/2P2PPB/7P/1K6 b - - 0 33',
    '3r3r/1R3p1p/Q5p1/1p6/2q5/2k2PPB/7P/1K6 w - - 0 34',
    '3r3r/1R3p1p/6p1/1p6/2q5/2k2PPB/7P/QK6 b - - 1 34',
    '3r3r/1R3p1p/6p1/1p6/2q5/5PPB/3k3P/QK6 w - - 2 35',
    '3r3r/1R3p1p/6p1/1p6/2q5/5PPB/1Q1k3P/1K6 b - - 3 35',
    '3r3r/1R3p1p/6p1/1p6/2q5/5PPB/1Q5P/1K1k4 w - - 4 36',
    '3r3r/1R3p1p/6p1/1p6/2q5/5PP1/1Q5P/1K1k1B2 b - - 5 36',
    '7r/1R3p1p/6p1/1p6/2q5/5PP1/1Q1r3P/1K1k1B2 w - - 6 37',
    '7r/3R1p1p/6p1/1p6/2q5/5PP1/1Q1r3P/1K1k1B2 b - - 7 37',
    '7r/3r1p1p/6p1/1p6/2q5/5PP1/1Q5P/1K1k1B2 w - - 0 38',
    '7r/3r1p1p/6p1/1p6/2B5/5PP1/1Q5P/1K1k4 b - - 0 38',
    '7r/3r1p1p/6p1/8/2p5/5PP1/1Q5P/1K1k4 w - - 0 39',
    '7Q/3r1p1p/6p1/8/2p5/5PP1/7P/1K1k4 b - - 0 39',
    '7Q/5p1p/6p1/8/2p5/3r1PP1/7P/1K1k4 w - - 1 40',
    'Q7/5p1p/6p1/8/2p5/3r1PP1/7P/1K1k4 b - - 2 40',
    'Q7/5p1p/6p1/8/8/2pr1PP1/7P/1K1k4 w - - 0 41',
    '8/5p1p/6p1/8/Q7/2pr1PP1/7P/1K1k4 b - - 1 41',
    '8/5p1p/6p1/8/Q7/2pr1PP1/7P/1K2k3 w - - 2 42',
    '8/5p1p/6p1/8/Q4P2/2pr2P1/7P/1K2k3 b - - 0 42',
    '8/7p/6p1/5p2/Q4P2/2pr2P1/7P/1K2k3 w - - 0 43',
    '8/7p/6p1/5p2/Q4P2/2pr2P1/7P/2K1k3 b - - 1 43',
    '8/7p/6p1/5p2/Q4P2/2p3P1/3r3P/2K1k3 w - - 2 44',
    '8/Q6p/6p1/5p2/5P2/2p3P1/3r3P/2K1k3 b - - 3 44'
    ]

time_moves(test_fens)