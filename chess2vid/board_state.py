from chess import SQUARES, Square, square_name

from chess2vid.blender import PieceObject
from chess2vid.exceptions import NoPieceError


class BoardState:

    def __init__(self):
        self.__pieces: list[PieceObject | None] = [None for i in range(len(SQUARES))]

    def set_piece(self, square: Square, piece: PieceObject):
        if not piece:
            raise ValueError(f"Can't set None to square {square_name(square)}")
        self.__pieces[square] = piece

    def get_piece(self, square: Square) -> PieceObject:
        piece = self.__pieces[square]
        if piece:
            return piece

        raise NoPieceError(f"At {square_name(square)}")

    def get_piece_or_none(self, square: Square) -> PieceObject | None:
        return self.__pieces[square]

    def remove_piece(self, square: Square):
        self.__pieces[square] = None

    def move_piece(self, from_square: Square, to_square: Square):
        self.__pieces[to_square] = self.__pieces[from_square]
        self.__pieces[from_square] = None
