from typing import Tuple
from chess import Square, square_file, square_rank

CELL_SIZE = 1


def square_location(square: Square) -> Tuple[int, int]:
    return (square_file(square) * CELL_SIZE, square_rank(square) * CELL_SIZE)
