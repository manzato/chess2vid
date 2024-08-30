from abc import abstractmethod
import bpy
from chess import BISHOP, BLACK, KING, KNIGHT, PAWN, QUEEN, ROOK

from chess2vid.material import apply_material


class PieceFactory:

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

    def __init__(self, base_path: str):
        self.__base_path = base_path

    def __build_piece_from_stl(self, file_path: str):
        stl_file = f"{self.__base_path}/{file_path}"
        bpy.ops.wm.stl_import(filepath=stl_file, global_scale=0.04)
        return bpy.context.active_object

    def create_piece(self, piece_type, color):
        piece = self.__build_piece_from_stl(self.piece_type_to_stl.get(piece_type))

        if color == BLACK:
            # Rotate black pieces, assuming their looking to the "front" for white
            bpy.ops.transform.rotate(value=3.14, orient_axis="Z", orient_type="GLOBAL")

        apply_material(color, piece)

        return piece
