import argparse
from ast import arg
import os
import bpy
import shutil

from chess2vid.chess2vid import Chess2Vid


ap = argparse.ArgumentParser()

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
ap.add_argument(
    "-o",
    "--output-path",
    default="./",
    help="Path to save rendered frames",
)
ap.add_argument("-stl", "--stl-path", help="Path to load stl files from")
ap.add_argument(
    "-s",
    "--save-blender",
    default=None,
    help="Path to store the generated blender file",
)
ap.add_argument(
    "-r",
    "--render-frames",
    help="Frames to render",
)


def main():

    args = vars(ap.parse_args())

    blender_bin = args.pop("blender_bin")

    if not blender_bin:
        blender_bin = shutil.which("blender")
        if not blender_bin:
            print("Error: NO blender found!")
    bpy.app.binary_path = blender_bin

    print(f"Using blender at '{blender_bin}'")

    if not args["stl_path"]:
        args["stl_path"] = os.path.join(os.getcwd(), "resources/stl/default")

    save_blender = args.pop("save_blender")

    render_frames = args.pop("render_frames")

    c2v = Chess2Vid(**args)

    c2v.setup()

    c2v.create_frames()

    if save_blender:
        # Don't leave anything selected, this is just for the saved blend file
        bpy.ops.object.select_all(action="DESELECT")

        print(f"Saving generated blender to {save_blender}")
        bpy.ops.wm.save_as_mainfile(filepath=save_blender)

    if render_frames:
        [start, end] = render_frames.split(":")
        c2v.render(int(start) if start else None, int(end) if end else None)
