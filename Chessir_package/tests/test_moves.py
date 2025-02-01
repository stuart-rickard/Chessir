
import unittest

from Chessir_package.src.Chessir.moves import MOVES, RAYS_FROM_TARGET


class MovesTest(unittest.TestCase):

    def test_moves(self):
        global MOVES

        # test that all the pieces are in the dictionary
        for piece in 'kqbnrpKQBNRP':
            self.assertIn(piece, MOVES)

            # test that every starting position is in the dictionary
            for idx in range(64):
                self.assertIsNotNone(MOVES[piece][idx])

                # test ordering of moves in each ray (should radiate out
                # from the starting index)
                for ray in MOVES[piece][idx]:
                    sorted_ray = sorted(ray, key=lambda x: abs(x - idx))
                    self.assertEqual(ray, sorted_ray)

        # verify that castling moves are present
        self.assertIn(6, MOVES['k'][4][0])
        self.assertIn(2, MOVES['k'][4][1])
        self.assertIn(62, MOVES['K'][60][0])
        self.assertIn(58, MOVES['K'][60][4])

    def test_rays_from_target(self):
        global RAYS_FROM_TARGET

        # test that both colors are in the dictionary
        for color in 'wb':
            self.assertIn(color, RAYS_FROM_TARGET)

            # test that all pieces that can attack the opposing color are in the dictionary
            if color == 'w':
                pieces = 'kqrbnp'
            if color == 'b':
                pieces = 'KQRBNP'

                for piece in pieces:
                    self.assertIn(piece, RAYS_FROM_TARGET[color])

                    # test that every starting position is in the dictionary
                    for idx in range(64):
                        self.assertIsNotNone(RAYS_FROM_TARGET[color][piece][idx])

                        # test ordering of moves in each ray (should radiate out
                        # from the starting index)
                        for ray in RAYS_FROM_TARGET[color][piece][idx]:
                            sorted_ray = sorted(ray, key=lambda x: abs(x - idx))
                            self.assertEqual(ray, sorted_ray)

        # verify that castling moves are not present in the kings' RAYS_FROM_TARGET
        self.assertNotIn(6, RAYS_FROM_TARGET['w']['k'][4][0])
        self.assertNotIn(2, RAYS_FROM_TARGET['w']['k'][4][1])
        self.assertNotIn(62, RAYS_FROM_TARGET['b']['K'][60][0])
        self.assertNotIn(58, RAYS_FROM_TARGET['b']['K'][60][4])

