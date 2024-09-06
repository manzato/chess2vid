import bpy

from chess2vid.actions import Action


class Animator:

    def __init__(self, verbose: bool, starting_frame=1):
        self.__verbose = verbose
        self.__current_frame = starting_frame
        self.__total_frames = starting_frame

    def animateAction(self, action: Action):
        frames = action.animate(self.__current_frame)

        if self.__verbose:
            print(
                f"Action {action} frames: {self.__current_frame}-{self.__current_frame + frames}"
            )
        self.__current_frame = self.__current_frame + frames
        self.__total_frames = self.__total_frames + frames
        bpy.context.scene.frame_end = self.__total_frames

    def get_total_frames(self) -> int:
        return self.__total_frames
