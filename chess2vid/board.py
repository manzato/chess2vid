import os
import bpy

from chess.pgn import Game
from chess import (
    BLACK,
    C1,
    C8,
    E1,
    E8,
    FILE_NAMES,
    G1,
    G8,
    KING,
    SQUARES,
    WHITE,
    Board,
    Color,
    Move,
    PieceType,
    Square,
    piece_name,
    square_name,
)
import chess

from chess2vid.actions import Action, CastleAction, MoveAction, TakeAction
from chess2vid.animator import Animator
from chess2vid.location import square_location
from chess2vid.material import apply_material
from chess2vid.piece_factory import PieceFactory


def square_color(square: Square) -> Color:
    base = square & 0x01 == 0x01
    invert = square & 0x08 == 0x08

    if base:
        return BLACK if invert else WHITE
    else:
        return WHITE if invert else BLACK


def _get_piece_obj_name(piece_type: PieceType, color, square: Square):
    name = "White_" if color == WHITE else "Black_"
    name += piece_name(piece_type)
    name += "_" + chess.square_name(square).upper()
    return name


def _is_castle(board: Board, move: Move):
    if board.piece_type_at(move.from_square) != KING:
        return False

    if move.from_square == E1 and move.to_square in [G1, C1]:
        return True

    if move.from_square == E8 and move.to_square in [G8, C8]:
        return True

    return False


class ChessBoard:
    def __init__(self, piece_factory: PieceFactory):
        self.__pieces: list[int] = [None for i in range(len(SQUARES))]
        self.__scale = 1
        self.__piece_factory = piece_factory
        self.__cell_size = 1 * self.__scale

    def __get_index(self, file: str, rank: int):
        return 8 * FILE_NAMES.index(file) + (rank - 1)

    def set_piece_at_index(self, index: int, piece):
        self.__pieces[index] = piece

    def set_piece(self, file: str, rank: int, piece):
        self.set_piece_at_index(self.__get_index(file, rank), piece)

    def get_piece_at_index(self, index: int):
        return self.__pieces[index]

    def get_piece(self, file: str, rank: int):
        return self.get_piece_at_index(self.__get_index(file, rank))

    def remove_piece(self, file: str, rank: int):
        self.__pieces[self.__get_index(file, rank)] = None

    def move_piece(self, file: str, rank: int, new_file: str, new_rank: int):
        piece = self.get_piece(file, rank)
        self.set_piece(new_file, new_rank, piece)
        self.remove_piece(file, rank)

    def create_piece(self, piece_type, color, square: Square):
        piece = self.__piece_factory.create_piece(piece_type, color)
        piece.location = square_location(square) + (0,)
        piece.name = _get_piece_obj_name(piece_type, color, square)
        apply_material(color, piece)
        self.__pieces[square] = piece
        return piece

    def draw_cell(self, square: Square):
        location = square_location(square) + (-0.1,)
        bpy.ops.mesh.primitive_cube_add(
            size=self.__cell_size, location=location, scale=(1, 1, 0.209)
        )
        cell = bpy.context.active_object
        cell.name = square_name(square).upper()
        apply_material(square_color(square), cell)

    def draw_board(self) -> None:
        for square in SQUARES:
            self.draw_cell(square)

    def _get_action_from_move(self, board: Board, move: Move) -> Action:
        target_occupant = self.__pieces[move.to_square]
        piece = self.__pieces[move.from_square]

        # TODO: Handle promotions
        # TODO: Handle "en passant"

        # Update board state
        # TODO: Remove taken piece?
        self.__pieces[move.to_square] = piece
        self.__pieces[move.from_square] = None

        if _is_castle(board, move):
            return CastleAction(move.from_square, move.to_square, piece)

        if target_occupant:
            return TakeAction(move.from_square, move.to_square, piece, move.promotion)
        else:
            return MoveAction(move.from_square, move.to_square, piece, move.promotion)

    def _initial_piece_setup(self, board: Board) -> None:
        for square, piece in board.piece_map().items():
            self.create_piece(piece.piece_type, piece.color, square)

    def recreate_game(self, game: Game):

        self._initial_piece_setup(game.board())

        animator = Animator()

        board = game.board()

        for move in game.mainline_moves():
            action = self._get_action_from_move(board, move)

            animator.animateAction(action)

    def render_frames(self, path):
        scene = bpy.context.scene

        for frame in range(655, 656):
            print(f"Rendering frame {frame}!")
            scene.frame_current = frame
            scene.render.filepath = os.path.join(path, str(frame))
            bpy.ops.render.render(write_still=True)
