import bpy

from chess2vid.actions import Action


class Animator:

    def __init__(self, starting_frame=1):
        self.__current_frame = starting_frame
        self.__total_frames = starting_frame

    def animateAction(self, action: Action):
        frames = action.animate(self.__current_frame)

        self.__current_frame = self.__current_frame + frames
        self.__total_frames = self.__total_frames + frames
        bpy.context.scene.frame_end = self.__total_frames
