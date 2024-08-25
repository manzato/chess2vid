import argparse
import bpy
import shutil

import chess

from chess import PAWN

from chess2vid.obtain import get_game 
from chess2vid.chess2vid import Chess2Vid


ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-fw", "--frame-width", type=int, default=480, help="Width of the resulting frames")
ap.add_argument("-fh", "--frame-height", type=int, default=360, help="Height of the resulting frames")
ap.add_argument("-fps", "--frames-per-second", type=int, default=30, help="Frames per second")
ap.add_argument("-i", "--input-game", required=True, help="Source game to convert")



def main():

    args = ap.parse_args()

    blender_bin = shutil.which("blender")
    blender_bin = "/home/manzato/projects/tools/blender-4.0.2-linux-x64/blender"
    if blender_bin:
        print("Found:", blender_bin)
        bpy.app.binary_path = blender_bin
    else:
        print("Unable to find blender!")


    c2v = Chess2Vid(**vars(args))

    """
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <chess_game.pgn>")
        sys.exit(1)
    
    file_name = sys.argv[1]

    game = get_game(file_name=file_name)

    n = 1
    for node in game.mainline():
        print(f"{str(n)}: ", end="")
        print(node.move)
        print(node.move.from_square)
        n = n + 1

    """
    """
    node = game.next()
    n = 1
    while node is not None:
        print(n)
        print(node.san() + " " + node.move.uci())
        print(node.move.from_square.)
        if node.move.drop is not None:
            print("DROPPPPP")

        node = node.next()
        n=n+1
    """
