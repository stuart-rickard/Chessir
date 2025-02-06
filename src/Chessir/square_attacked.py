from .moves import RAYS_FROM_TARGET

"""
The square_attacked function determines whether a given square is attacked by an opponent's piece.

If the get_details parameter is set to True, it will return 1) the indices of attacking pieces and their ray of attack and 2) the indices of pinned pieces and the indices to which they can move without exposing the given square.

Please note this function does not have the capability to determine whether a pawn can be attacked by an en passant move by the opponent.

There's an opportunity to make this faster: rook and bishop checks could cover queen, because queen attacks along those rays, thus negating the need to separately check queen attack rays
"""

def square_attacked(board, square_index, player='w', get_details=False):

    res = {
        'attacked': False,
        'attack_info': [], # elements will be [attacking_piece_index, [attacking_ray_indices]]
        'pins_info': [] # elements will be [pinned_piece_index, [allowed_move_indices]]
        }

    # list the types of pieces from which we are checking for attacks
    pieces = list(RAYS_FROM_TARGET[player].keys())

    for piece in pieces:
        rays_list = RAYS_FROM_TARGET[player].get(piece)[square_index] 
        for ray in rays_list: # go through the rays for that piece at that square
            for i in range(len(ray)): # proceed outward along the ray
                end = ray[i]
                end_piece = board.get_piece(end)
                if end_piece == ' ': 
                    continue # if there's no piece at end, go to next index in ray
                else: # there is a piece at end
                    if end_piece == piece: # end_piece can attack on this ray, so square_index is attacked
                        res['attacked'] = True
                        if not get_details:
                            return res
                        res['attack_info'].append([end, ray[:i+1]])
                        break # attacking piece was found; don't need to continue along the ray
                    if (player == 'w' and end_piece.isupper()) or (player == 'b' and end_piece.islower()):
                        # this is a friendly and possibly pinned piece, continue along the ray and see whether there is an opponent piece that matches piece
                        pin_index = end
                        while (i + 1) < len(ray):
                            i += 1
                            end = ray[i]
                            end_piece = board.get_piece(end)
                            if end_piece == ' ':
                                continue
                            else: # not an empty square
                                if end_piece == piece:
                                    res['pins_info'].append([pin_index, ray[:i+1]]) # this is the index of the pinned piece and the indices it can move to
                                break # break the while loop because a piece was encountered; no need to continue along the ray
                    break # break the for i loop which is checking outward along the ray -- this is the case where end_piece belongs to the opponent but its type does not match piece; therefore no need to continue along the ray
    
    return res
