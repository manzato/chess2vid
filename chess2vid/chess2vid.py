import bpy

import chess.pgn

from chess2vid.blender import create_camera, create_light, create_material
from chess2vid.context import Context
from chess2vid.piece_factory import StlPieceFactory
from chess2vid.board import ChessBoard


def get_game(file_name: str) -> chess.pgn.Game:
    with open(file_name) as fd:
        return chess.pgn.read_game(fd)


class Chess2Vid:

    def __init__(
        self,
        frame_width: int,
        frame_height: int,
        frames_per_second: int,
        input_game: str,
        output_path: str,
        stl_path: str,
    ):
        self.__frame_width = frame_width
        self.__frame_height = frame_height
        self.__output_path = output_path
        self.__stl_path = stl_path

        # Start with an empty world (no camera, lights, etc)
        bpy.ops.wm.read_factory_settings(use_empty=True)

        self.__scale = 1
        self.__context = Context(
            create_material("white", [1, 1, 1, 1]),
            create_material("black", [0, 0, 0, 1]),
        )
        self.__game = get_game(file_name=input_game)

    def setup(self):
        """
        n = 1
        for node in game.mainline():
            print(f"{str(n)}: ", end="")
            print(node.move)
            print(node.move.from_square)
            n = n + 1
        """

        (camera, camera_target) = create_camera()
        create_light()

        self.__board = ChessBoard(
            StlPieceFactory(self.__context, self.__stl_path), self.__context
        )
        self.__board.initial_piece_setup(self.__game.board())

    def render(self):
        scene = bpy.context.scene
        scene.render.resolution_x = self.__frame_width
        scene.render.resolution_y = self.__frame_height

        self.__board.draw_board(self.__context)

        scene.render.filepath = f"{self.__output_path}/1.png"
        bpy.ops.render.render(write_still=True)
