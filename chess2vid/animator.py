from chess2vid.actions import Action
from chess2vid.board import ChessBoard


class Animator:

    def __init__(self, board: ChessBoard, starting_frame=1):
        self.__board = board
        self.__current_frame = starting_frame
        self.__total_frames = starting_frame

    def animate(self, actions: list[Action]):

        for action in actions:
            # self.__total_frames = self.__total_frames + frame_length

            action.animate(self.__board, self.__current_frame)

            # self.__current_frame = self.__current_frame + frame_length
