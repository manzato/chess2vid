import os
import bpy

import chess.pgn

from chess.pgn import Game

from chess2vid.blender import create_camera, create_light, create_material
from chess2vid.piece_factory import StlPieceFactory
from chess2vid.board import ChessBoard

from chess2vid.material import set_light_material, set_dark_material


def get_game(file_name: str) -> Game:
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

        set_light_material(create_material("white", [1, 1, 1, 1]))
        set_dark_material(create_material("black", [0, 0, 0, 1]))

        self.__game: Game = get_game(file_name=input_game)

    def setup(self):

        (camera, camera_target) = create_camera()
        create_light()

        self.__board = ChessBoard(StlPieceFactory(self.__stl_path))

    def create_frames(self):
        self.__board.recreate_game(self.__game)

    def render(self, start: int | None, end: int | None):
        scene = bpy.context.scene
        scene.render.resolution_x = self.__frame_width
        scene.render.resolution_y = self.__frame_height

        if not end:
            end = bpy.context.scene.frame_end

        print(f"RENDER from {start} to {end}")

        for frame in range(start, end + 1):
            print(f"Rendering frame {frame}!")
            scene.frame_current = frame
            scene.render.filepath = os.path.join(
                self.__output_path, f"{str(frame)}.png"
            )
            bpy.ops.render.render(write_still=True)
