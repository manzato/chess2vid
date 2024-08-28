import argparse
import os
import bpy
import shutil

from chess2vid.chess2vid import Chess2Vid


ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument(
    "-fw", "--frame-width", type=int, default=1920, help="Width of the resulting frames"
)
ap.add_argument(
    "-fh",
    "--frame-height",
    type=int,
    default=1080,
    help="Height of the resulting frames",
)
ap.add_argument(
    "-fps", "--frames-per-second", type=int, default=30, help="Frames per second"
)
ap.add_argument("-i", "--input-game", required=True, help="Source game to convert")
ap.add_argument("-b", "--blender-bin", help="Path to blender binary")
ap.add_argument("-o", "--output-path", default="./", help="Path to save output")
ap.add_argument("-stl", "--stl-path", help="Path to load stl files from")


def main():

    args = vars(ap.parse_args())

    blender_bin = args["blender_bin"]

    if not blender_bin:
        blender_bin = shutil.which("blender")
        if not blender_bin:
            print("Error: NO blender found!")
    bpy.app.binary_path = blender_bin

    del args["blender_bin"]
    print(f"Using blender at '{blender_bin}'")

    if not args["stl_path"]:
        args["stl_path"] = os.path.join(os.getcwd(), "resources/stl/default")

    c2v = Chess2Vid(**args)

    c2v.setup()

    c2v.create_frames()

    c2v.render()

    """
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

    # Don't leave anything selected, this is just for the saved blend file
    bpy.ops.object.select_all(action="DESELECT")

    bpy.ops.wm.save_as_mainfile(filepath="./save.blend")
