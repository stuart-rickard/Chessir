"""
The game module implements core Chessir class, `Game`, to control a chess
game.

Two additional classes are defined: `InvalidMove` -- a subclass of the base
`Exception` class, and `State` -- a namedtuple for handling game state
information.

Chessir has neither an *engine*, nor a *GUI*, and it cannot currently
handle any chess variants (e.g., Chess960) that are not equivalent to standard
chess rules.
"""

from collections import namedtuple, Counter

from src.Chessir.board import Board
from src.Chessir.moves import MOVES

import copy
from src.Chessir.square_attacked import square_attacked

# Define a named tuple with FEN field names to hold game state information
State = namedtuple('State', ['player', 'rights', 'en_passant', 'ply', 'turn'])


class InvalidMove(Exception):
    """
    Subclass base `Exception` so that exception handling doesn't have to
    be generic.
    """
    pass


class Game(object):
    """
    This class manages a chess game instance -- it stores an internal
    representation of the position of each piece on the board in an instance
    of the `Board` class, and the additional state information in an instance
    of the `State` namedtuple class.
    """

    NORMAL = 0
    CHECK = 1
    CHECKMATE = 2
    STALEMATE = 3
    DRAW = 4

    default_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    def __init__(self, fen=default_fen):
        """
        Initialize the game board to the supplied FEN state (or the default
        starting state if none is supplied), and determine whether to check
        the validity of moves .
        """
        self.board = Board()
        self.state = State(' ', ' ', ' ', ' ', ' ')
        self.move_history = []
        self.fen_history = []
        self.moves = None
        self.positions_count = Counter()
        self.set_fen(fen=fen)

    def __str__(self):
        """Return the current FEN representation of the game."""
        return ' '.join(str(x) for x in [self.board] + list(self.state))

    @staticmethod
    def i2xy(pos_idx):
        """
        Convert a board index to algebraic notation.
        """
        return chr(97 + pos_idx % 8) + str(8 - pos_idx // 8)

    @staticmethod
    def xy2i(pos_xy):
        """
        Convert algebraic notation to board index.
        """
        return (8 - int(pos_xy[1])) * 8 + (ord(pos_xy[0]) - ord('a'))

    def get_fen(self):
        """
        Get the latest FEN string of the current game.
        """
        return ' '.join(str(x) for x in [self.board] + list(self.state))

    def set_fen(self, fen):
        """
        Parse a FEN string into components and store in the `board` and `state`
        properties, and append the FEN string to the game history *without*
        clearing it first.
        """
        self.fen_history.append(fen)
        fields = fen.split(' ')
        fields[4] = int(fields[4])
        fields[5] = int(fields[5])
        self.state = State(*fields[1:])
        self.board.set_position(fields[0])
        # clear the move cache
        self.moves = None
        # increment the position count
        self.positions_count[fields[0]] += 1

    def reset(self, fen=default_fen):
        """
        Clear the game history and set the board to the default starting
        position.
        """
        self.move_history = []
        self.fen_history = []
        self.moves = None
        self.positions_count = Counter()
        self.set_fen(fen)

    def get_material_string(self):
        """
        Return a string listing the pieces on the board.
        """
        material_string = ''
        for idx in range(64):
            piece = self.board.get_piece(idx)
            if piece != ' ':
                material_string += piece
        return material_string

    def apply_move(self, move, validate=False):
        """
        Take a move in simple algebraic notation and apply it to the game.
        Note that simple algebraic notation differs from FEN move notation
        in that castling is not given any special notation, and pawn promotion
        piece is always lowercase.

        Update the state information (player, castling rights, en passant
        target, ply, and turn), apply the move to the game board, and
        update the game history.

        If the validate parameter is set to True, the move will be checked
        for legality before it is applied to the game. If the move is
        illegal, an `InvalidMove` exception is raised.
        """
        # declare the status fields using default parameters
        fields = ['w', 'KQkq', '-', 0, 1]

        # gracefully handle empty or incomplete moves
        if move is None or move == '' or len(move) < 4:
            raise InvalidMove("\nIllegal move: {}\nfen: {}".format(move,
                                                                   str(self)))

        # convert to lower case to avoid casing issues
        move = move.lower()

        start = Game.xy2i(move[:2])
        end = Game.xy2i(move[2:4])
        piece = self.board.get_piece(start)
        target = self.board.get_piece(end)

        if validate and move not in self.get_moves(idx_list=[start]):
            raise InvalidMove("\nIllegal move: {}\nfen: {}".format(move,
                                                                   str(self)))

        # toggle the active player
        fields[0] = {'w': 'b', 'b': 'w'}[self.state.player]

        # modify castling rights - the set of castling rights that *might*
        # be voided by a move is uniquely determined by the starting index
        # of the move - regardless of what piece moves from that position
        # (excluding chess variants like chess960).
        rights_map = {0: 'q', 4: 'kq', 7: 'k',
                      56: 'Q', 60: 'KQ', 63: 'K'}
        void_set = ''.join([rights_map.get(start, ''),
                           rights_map.get(end, '')])
        new_rights = [r for r in self.state.rights if r not in void_set]
        fields[1] = ''.join(new_rights) or '-'

        # set en passant target square when a pawn advances two spaces
        if piece.lower() == 'p' and abs(start - end) == 16:
            fields[2] = Game.i2xy((start + end) // 2)

        # reset the half move counter when a pawn moves or is captured
        fields[3] = self.state.ply + 1
        if piece.lower() == 'p' or target.lower() != ' ':
            fields[3] = 0

        # Increment the turn counter when the next move is from white, i.e.,
        # the current player is black
        fields[4] = self.state.turn
        if self.state.player == 'b':
            fields[4] = self.state.turn + 1

        # check for pawn promotion
        if len(move) == 5:
            piece = move[4]
            if self.state.player == 'w':
                piece = piece.upper()

        # record the move in the game history and apply it to the board
        self.move_history.append(move)
        self.board.move_piece(start, end, piece)

        # move the rook to the other side of the king in case of castling
        c_type = {62: 'K', 58: 'Q', 6: 'k', 2: 'q'}.get(end, None)
        if piece.lower() == 'k' and c_type and c_type in self.state.rights:
            coords = {'K': (63, 61), 'Q': (56, 59),
                      'k': (7, 5), 'q': (0, 3)}[c_type]
            r_piece = self.board.get_piece(coords[0])
            self.board.move_piece(coords[0], coords[1], r_piece)

        # in en passant remove the piece that is captured
        if piece.lower() == 'p' and self.state.en_passant != '-' \
                and Game.xy2i(self.state.en_passant) == end:
            ep_tgt = Game.xy2i(self.state.en_passant)
            if ep_tgt < 24:
                self.board.move_piece(end + 8, end + 8, ' ')
            elif ep_tgt > 32:
                self.board.move_piece(end - 8, end - 8, ' ')

        # state update must happen after castling
        self.set_fen(' '.join(str(x) for x in [self.board] + list(fields)))

        # clear the move cache
        self.moves = None

    def get_moves(self, player=None, idx_list=range(64)): 
        """
        Get a list containing the legal moves for pieces owned by the
        specified player that are located at positions included in the
        idx_list. By default, it compiles the list for the active player
        (i.e., self.state.player) by filtering the list of _all_moves() to
        eliminate any that would expose the player's king to check.
        """
        if self.moves is None:
            self.moves = self._all_moves(player=player, idx_list=idx_list)
        return self.moves

    def _all_moves(self, player=None, idx_list=range(64)):
        """
        Get a list containing all reachable moves for pieces owned by the
        specified player that are located at positions included in the idx_list. By
        default, it compiles the list for the active player (i.e.,
        self.state.player) by checking every square on the board.
        """

        player = player or self.state.player
        res_moves = []

        my_piece_starts_and_types = []
        for start in idx_list:
            piece = self.board.get_piece(start)
            if piece == ' ': 
                continue
            if player == 'w' and piece.islower():
                continue
            if player == 'b' and piece.isupper():
                continue
            if piece.lower() == 'k':
                my_piece_starts_and_types.insert(0, [start, piece]) # put king at the front of the list
            else:
                my_piece_starts_and_types.append([start, piece])

        king_attack_data = square_attacked(self.board, 
                                           my_piece_starts_and_types[0][0], # king index
                                           player, get_details=True)
        king_attack_list = king_attack_data['attack_info']
        pins_list = king_attack_data['pins_info']
        pinned_indices = {pin[0] for pin in pins_list}
        attack_path = {i for attack in king_attack_list for i in attack[1]}

        if len(king_attack_list) > 1: # double check
            my_piece_starts_and_types = [my_piece_starts_and_types[0]] # only the king can move
        elif len(king_attack_list) == 1: # single check
            # don't create moves for pinned pieces
            my_piece_starts_and_types = [piece for piece in my_piece_starts_and_types if piece[0] not in pinned_indices]

        for [start, piece] in my_piece_starts_and_types:

            # MOVES contains the list of all possible moves for a piece of
            # the specified type on an empty chess board.
            rays = MOVES.get(piece)

            # handle pinned pieces
            if start in pinned_indices:
                pin_data = next(pin for pin in pins_list if pin[0] == start)
                allowed_move_indices = pin_data[1] # these are the squares where the pinned piece can move (the index of the pinning piece and the indices along the ray of its attack toward the king)
                for ray in rays[start]:
                    # remove any values that are not in allowed_move_indices
                    ray = [i for i in ray if i in allowed_move_indices]
                    new_moves = self._trace_ray(start, piece, ray, player, king_attack_list, attack_path)
                    res_moves.extend(new_moves)
            else: # not pinned piece
                for ray in rays[start]:
                    # Trace each of the 8 (or fewer) possible directions that a
                    # piece at the given starting index could move
                    new_moves = self._trace_ray(start, piece, ray, player, king_attack_list, attack_path)
                    res_moves.extend(new_moves)

        return res_moves
    
    def _trace_ray(self, start, piece, ray, player, king_attack_list=None, attack_path=None):
        """
        Return a list of moves by filtering the supplied ray (a list of
        indices corresponding to end points that lie on a common line from
        the starting index) based on the state of the chess board (e.g.,
        castling, capturing, en passant, etc.). Moves are in simple algebraic
        notation, e.g., 'a2a4', 'g7h8q', etc.

        Each ray should be an element from Chessir.MOVES, representing all
        the moves that a piece could make from the starting square on an
        otherwise blank chessboard. This function filters the moves in a ray
        by enforcing the rules of chess for the legality of capturing pieces,
        castling, en passant, and pawn promotion.
        """
        res_moves = []

        for end in ray:
            sym = piece.lower()
            del_x = abs(end - start) % 8
            move = [Game.i2xy(start) + Game.i2xy(end)]
            tgt_owner = self.board.get_owner(end)

            # Abort if the current player owns the piece at the end point
            if tgt_owner == player:
                break

            # Abort king moves that would put it in check
            if sym == 'k':
                new_board = copy.deepcopy(self.board)
                new_board.move_piece(start, end, piece)
                if square_attacked(new_board, end, player=player)['attacked']:
                    break

            # Test castling of king
            if sym == 'k' and del_x == 2:
                if king_attack_list:
                    # No castling if king is currently in check
                    break 
                gap_owner = self.board.get_owner((start + end) // 2)
                out_owner = self.board.get_owner(end - 1)
                rights = {62: 'K', 58: 'Q', 6: 'k', 2: 'q'}.get(end, ' ')
                if (tgt_owner or gap_owner or rights not in self.state.rights or
                        (rights.lower() == 'q' and out_owner)):
                    # Abort castling because missing castling rights
                    # or piece in the way
                    break
                # Castling not allowed if path square is attacked
                if square_attacked(self.board, (start + end) // 2, player=player)['attacked']:
                    break

            if sym == 'p':
                # Pawns cannot move forward to an occupied square
                if del_x == 0 and tgt_owner:
                    break

                # Test en passant exception for pawn
                elif del_x != 0 and not tgt_owner:
                    ep_coords = self.state.en_passant
                    if ep_coords == '-' or end != Game.xy2i(ep_coords):
                        break

                # Pawn promotions need to list all possible promotions
                if (end < 8 or end > 55):
                    move = [move[0] + s for s in ['b', 'n', 'r', 'q']]            

            # When king is in check other pieces can only move to block or capture checking piece
            if attack_path and piece.lower() != 'k': 
                if end not in attack_path:
                    # Empty the move list if the piece cannot block or capture the checking piece, but don't break because the tgt_owner check below is needed to stop searching along the ray
                    move = [] 

            res_moves.extend(move)

            # break ray search when an opponent piece is encountered
            if tgt_owner:

                break

        return res_moves
    
    @property
    def status(self):

        k_sym, opp = {'w': ('K', 'b'), 'b': ('k', 'w')}.get(self.state.player)
        k_loc = Game.i2xy(self.board.find_piece(k_sym))
        can_move = len(self.get_moves())
        is_exposed = [m[2:4] for m in self._all_moves(player=opp)
                      if m[2:4] == k_loc]
        ply = self.state.ply
        material_count = Counter(self.get_material_string())
        three_fold = max(self.positions_count.values()) >= 3


        status = Game.NORMAL
        if is_exposed:
            status = Game.CHECK
            if not can_move:
                status = Game.CHECKMATE
        elif not can_move:
            status = Game.STALEMATE
        
        if status == Game.NORMAL: # check for other draw conditions
            if ply >= 100:
                status = Game.DRAW
            else:
                # insufficient material
                # check for pieces other than kings, knights, and bishops
                if not set(material_count) - {'k', 'K', 'n', 'N', 'b', 'B'}:
                    # check for insufficient bishops and knights
                    if (material_count['n'] /2 + material_count['b'] <= 1 and material_count['N'] /2 + material_count['B'] <= 1):
                        status = Game.DRAW

        if three_fold:
            status = Game.DRAW                        

        return status
