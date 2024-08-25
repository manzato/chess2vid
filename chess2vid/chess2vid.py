import bpy

import chess

from chess import PAWN

class Chess2Vid:

    def __init__(self, frame_width: int, frame_height: int, frames_per_second: int, input_game: str):
        # Start with an empty world (no camera, lights, etc)
        #bpy.ops.wm.read_factory_settings(use_empty=True)

        scene = bpy.context.scene
        scene.render.filepath = '/tmp/1.png'
        bpy.ops.render.render(write_still=True)
