from chess import SQUARES, Square

from chess2vid.blender import PieceObject


class BoardState:

    def __init__(self):
        self.__pieces: list[int] = [None for i in range(len(SQUARES))]

    def set_piece(self, square: Square, piece: PieceObject):
        self.__pieces[square] = piece

    def get_piece(self, square: Square) -> PieceObject | None:
        return self.__pieces[square]

    def remove_piece(self, square: Square):
        self.__pieces[square] = None

    def move_piece(self, from_square: Square, to_square: Square):
        self.__pieces[to_square] = self.__pieces[from_square]
        self.__pieces[from_square] = None
