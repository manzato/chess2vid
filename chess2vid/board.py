import os
import bpy

from chess import (
    BLACK,
    FILE_NAMES,
    RANK_NAMES,
    WHITE,
    Board,
    Square,
    piece_name,
)
import chess

from chess2vid.blender import apply_material
from chess2vid.context import Context
from chess2vid.piece_factory import PieceFactory


class ChessBoard:
    def __init__(self, piece_factory: PieceFactory, context: Context):
        self.__pieces: list[int] = [None for i in range(64)]
        self.__scale = 1
        self.__piece_factory = piece_factory
        self.__cell_size = 1 * self.__scale
        self.__context = context

    def __get_index(self, file: str, rank: int):
        return 8 * FILE_NAMES.index(file) + (rank - 1)

    def get_2d_location(self, file: str, rank: int):
        return (self.__cell_size * FILE_NAMES.index(file), self.__cell_size * rank)

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

    def __apply_material(self, color, object):
        apply_material(
            object,
            (
                self.__context.light_material
                if color == WHITE
                else self.__context.dark_material
            ),
        )

    def __create_cell(self, color, file: str, rank: int):
        bpy.ops.mesh.primitive_cube_add(
            size=self.__cell_size,
            location=self.get_2d_location(file, rank) + (-0.1,),
            scale=(1, 1, 0.209),
        )
        cell = bpy.context.active_object
        cell.name = f"{file}{str(rank)}"
        self.__apply_material(color, cell)

    def __get_piece_obj_name(self, piece_type, color, square: Square):
        name = "White_" if color == WHITE else "Black_"
        name += piece_name(piece_type)
        name += "_" + chess.square_name(square).upper()
        return name

    def create_piece(self, piece_type, color, square: Square):
        piece = self.__piece_factory.create_piece(piece_type, color)
        piece.location = self.__context.square_position(square) + (0,)
        piece.name = self.__get_piece_obj_name(piece_type, color, square)
        self.__apply_material(color, piece)
        return piece

    def create_cell(self, color, file: str, rank: int):
        return self.__create_cell(color, file, rank)

    def create_board(self):
        color = WHITE
        for file in FILE_NAMES:
            color = BLACK if color == WHITE else WHITE
            for rank in RANK_NAMES:
                color = BLACK if color == WHITE else WHITE
                self.create_cell(color, file, rank)

    def draw_cell(self, color, file: str, rank: str):
        location = self.__context.get_2d_location(file, rank) + (-0.1,)
        bpy.ops.mesh.primitive_cube_add(
            size=self.__cell_size, location=location, scale=(1, 1, 0.209)
        )
        cell = bpy.context.active_object
        cell.name = f"{file}{str(rank)}"
        self.__apply_material(color, cell)

    def draw_board(self, context: Context) -> None:
        color = WHITE
        for file in FILE_NAMES:
            color = BLACK if color == WHITE else WHITE
            for rank in RANK_NAMES:
                color = BLACK if color == WHITE else WHITE
                self.draw_cell(color, file, rank)

    def initial_piece_setup(self, board: Board) -> None:
        for square, piece in board.piece_map().items():
            self.create_piece(piece.piece_type, piece.color, square)

    def recreate_game(self, game):
        """
        animator = Animator(self)

        for node in game.mainline():
            animator.animate(node)

        self.render_frames("/home/manzato/projects/chess2vid/rendered_frames/")


        print("Finished recreating game")
        """
        pass

    def render_frames(self, path):
        scene = bpy.context.scene

        for frame in range(655, 656):
            print(f"Rendering frame {frame}!")
            scene.frame_current = frame
            scene.render.filepath = os.path.join(path, str(frame))
            bpy.ops.render.render(write_still=True)
