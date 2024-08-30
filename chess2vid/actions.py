from abc import ABC, abstractmethod
from chess import Square

from chess2vid.location import square_location

FRAMES_PER_MOVE = 10


class Action(ABC):

    @abstractmethod
    def animate(self, current_frame: int) -> int:
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

    def __init__(
        self, source: Square, target: Square, piece, promoted_to_piece_type=None
    ):
        super().__init__(source, target, piece)
        self._promoted_to_piece_type = promoted_to_piece_type

    def animate(self, current_frame: int) -> int:
        # TODO: Handle knights (nice L shaped move, vs straight diagonal)
        # Starting position of the piece for this animation
        self.piece.keyframe_insert("location", frame=current_frame)

        target_location = square_location(self.target)

        self.piece.location.x = target_location[0]
        self.piece.location.y = target_location[1]

        self.piece.keyframe_insert("location", frame=current_frame + FRAMES_PER_MOVE)

        return FRAMES_PER_MOVE

    def __str__(self) -> str:
        return f"Move {self.piece.name} from {self.source} to {self.target}"


class TakeAction(MoveAction):

    def __str__(self) -> str:
        return f"Take {self.source} to {self.target}"


class CastleAction(MoveAction):

    def __str__(self) -> str:
        return f"Castle {self.source} to {self.target}"
