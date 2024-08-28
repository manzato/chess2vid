from abc import ABC, abstractmethod
from chess import Square

from chess2vid.board import ChessBoard

FRAMES_PER_MOVE = 30


class Action(ABC):

    @abstractmethod
    def animate(self, board: ChessBoard, current_frame: int) -> int:
        pass


class BaseAction(Action):

    def __init__(self, source: Square, target: Square, piece):
        self.__source = source
        self.__target = target
        self.__piece = piece

    @property
    def source(self):
        return self.__source

    @property
    def target(self):
        return self.__target

    @property
    def piece(self):
        return self.__piece


class MoveAction(BaseAction):

    def animate(self, board: ChessBoard, current_frame: int) -> int:
        # Starting position of the piece for this animation
        self.piece.keyframe_insert("location", frame=current_frame)

    def __str__(self) -> str:
        return f"Move {self.piece.name} from {self.source} to {self.target}"


class TakeAction(BaseAction):

    def __str__(self) -> str:
        return f"Take {self.source} to {self.target}"
