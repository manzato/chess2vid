from typing import Tuple
from chess import FILE_NAMES, RANK_NAMES, Square, square_file, square_rank


class Context:

    def __init__(self, light_material, dark_material):
        self.__light_material = light_material
        self.__dark_material = dark_material
        self.__scale = 1
        self.__cell_size = 1 * self.__scale

    @property
    def light_material(self):
        return self.__light_material

    @property
    def dark_material(self):
        return self.__dark_material

    @property
    def scale(self):
        return self.__scale

    def get_2d_location(self, file: str, rank: str):
        return (
            self.__cell_size * FILE_NAMES.index(file),
            self.__cell_size * RANK_NAMES.index(rank),
        )

    def square_position(self, square: Square) -> Tuple[int, int]:
        return (
            square_file(square) * self.__cell_size,
            square_rank(square) * self.__cell_size,
        )
