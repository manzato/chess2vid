from abc import abstractmethod
from os import path
import bpy
from chess import BISHOP, BLACK, KING, KNIGHT, PAWN, QUEEN, ROOK, WHITE

from chess2vid.blender import apply_material
from chess2vid.context import Context


class PieceFactory:

    def __init__(self, context: Context):
        self.__context = context

    @property
    def context(self):
        return self.__context

    @property
    def scale(self):
        return self.__context.scale

    @abstractmethod
    def create_piece(self, piece_type):
        pass


class StlPieceFactory(PieceFactory):
    piece_type_to_stl = {
        PAWN: "pawn.stl",
        KNIGHT: "knight.stl",
        BISHOP: "bishop.stl",
        ROOK: "rook.stl",
        QUEEN: "queen.stl",
        KING: "king.stl",
    }

    def __init__(self, context: Context, base_path: str):
        super().__init__(context)
        self.__base_path = base_path

    def __build_piece_from_stl(self, file_path: str):
        stl_file = f"{self.__base_path}/{file_path}"
        print(f"Loading '{stl_file}'")
        bpy.ops.wm.stl_import(filepath=stl_file, global_scale=0.04 * self.scale)
        return bpy.context.active_object

    def create_piece(self, piece_type, color):
        piece = self.__build_piece_from_stl(self.piece_type_to_stl.get(piece_type))

        if color == BLACK:
            # Rotate black pieces, assuming their looking to the "front" for white
            bpy.ops.transform.rotate(value=3.14, orient_axis="Z", orient_type="GLOBAL")

        apply_material(
            piece,
            (
                self.context.light_material
                if color == WHITE
                else self.context.dark_material
            ),
        )

        return piece
