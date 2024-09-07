from abc import ABC, abstractmethod
from chess import (
    A1,
    A8,
    C1,
    C8,
    D1,
    D8,
    F1,
    F8,
    G1,
    G8,
    H1,
    H8,
    WHITE,
    Color,
    PieceType,
    Square,
    piece_name,
    square_name,
)
import bpy

from chess2vid.blender import PieceObject
from chess2vid.board_state import BoardState
from chess2vid.location import CELL_SIZE, square_location
from chess2vid.material import apply_material
from chess2vid.piece_factory import PieceFactory

FRAMES_PER_MOVE = 30


def _get_piece_obj_name(piece_type: PieceType, color, square: Square):
    name = "White_" if color == WHITE else "Black_"
    name += piece_name(piece_type)
    name += "_" + square_name(square).upper()
    return name


class Action(ABC):

    @abstractmethod
    def apply(self, boardState: BoardState):
        pass

    @abstractmethod
    def animate(self, current_frame: int) -> int:
        pass


class DrawSquareAction(Action):

    def __init__(self, square: Square, color: Color):
        self.__square = square
        self.__color = color
        self.__name = square_name(self.__square).upper()

    def apply(self, board_state: BoardState):
        pass

    def animate(self, current_frame: int) -> int:
        location = square_location(self.__square) + (-0.1,)
        bpy.ops.mesh.primitive_cube_add(
            size=CELL_SIZE, location=location, scale=(1, 1, 0.209)
        )
        cell = bpy.context.active_object
        cell.name = self.__name
        apply_material(self.__color, cell)

        return 0

    def __str__(self) -> str:
        return f"DrawSquare {self.__name}"


class PlacePieceAction(Action):

    def __init__(
        self,
        square: Square,
        piece_type: PieceType,
        color: Color,
        piece_factory: PieceFactory,
    ):
        self.__square = square
        self.__color = color
        self.__piece_type = piece_type
        self.__piece_factory = piece_factory

    def apply(self, board_state: BoardState):
        piece = self.__piece_factory.create_piece(self.__piece_type, self.__color)
        piece.location = square_location(self.__square) + (0,)
        piece.name = _get_piece_obj_name(self.__piece_type, self.__color, self.__square)
        apply_material(self.__color, piece)

        board_state.set_piece(self.__square, piece)

    def animate(self, current_frame: int) -> int:
        # Could animate the piece "fade-in" if one woud want
        return 0

    def __str__(self) -> str:
        return f"Place {self.__piece_type} at {self.__square}"


class BaseAction(Action):

    def __init__(self, source: Square, target: Square, piece: PieceObject):
        self.__source = source
        self.__target = target
        self.__piece = piece

    def apply(self, board_state: BoardState):
        pass

    @property
    def source(self):
        return self.__source

    @property
    def target(self):
        return self.__target

    @property
    def piece(self):
        return self.__piece


def _animate_move(piece: PieceObject, new_square: Square, current_frame: int) -> None:
    """Animates a piece move simply sending it in a straight line to the target square"""
    # TODO: Handle knights (nice L shaped move, vs straight diagonal)

    # Start position of the piece for this animation
    piece.keyframe_insert("location", frame=current_frame)

    target_location = square_location(new_square)

    piece.location.x = target_location[0]
    piece.location.y = target_location[1]

    # Finish position of the piece for this animation
    piece.keyframe_insert("location", frame=current_frame + FRAMES_PER_MOVE)


class MoveAction(BaseAction):

    def __init__(
        self, source: Square, target: Square, piece, promoted_to_piece_type=None
    ):
        super().__init__(source, target, piece)
        self._promoted_to_piece_type = promoted_to_piece_type

    def apply(self, board_state: BoardState):
        board_state.move_piece(self.source, self.target)

    def animate(self, current_frame: int) -> int:
        _animate_move(self.piece, self.target, current_frame)
        return FRAMES_PER_MOVE

    def __str__(self) -> str:
        name = self.piece.name if self.piece else "None"
        return (
            f"Move {name} from {square_name(self.source)} to {square_name(self.target)}"
        )


class TakeAction(MoveAction):

    def apply(self, board_state: BoardState):
        self.__old_piece = board_state.get_piece(self.target)
        super().apply(board_state)

    def animate(self, current_frame: int) -> int:
        self.__old_piece.keyframe_insert("location", frame=current_frame)
        # FIXME: A taken piece "disapears" under the board... lame...
        self.__old_piece.location.z = -2 * CELL_SIZE
        self.__old_piece.keyframe_insert(
            "location", frame=current_frame + FRAMES_PER_MOVE
        )

        return super().animate(current_frame)

    def __str__(self) -> str:
        name = self.piece.name if self.piece else "None"
        return f"{name} takes from {square_name(self.source)} to {square_name(self.target)}"


class CastleAction(BaseAction):

    def __init__(self, source: Square, target: Square, piece: PieceObject):
        super().__init__(source, target, piece)
        self.__rook_piece: PieceObject | None = None

        if target == G1:
            self.__rook_source = H1
            self.__rook_target = F1
        elif target == C1:
            self.__rook_source = A1
            self.__rook_target = D1
        elif target == G8:
            self.__rook_source = H8
            self.__rook_target = F8
        elif target == C8:
            self.__rook_source = A8
            self.__rook_target = D8
        else:
            raise ValueError(f"Castle with target square {target} is invalid!")

    def apply(self, board_state: BoardState):
        self.__rook_piece = board_state.get_piece(self.__rook_source)
        board_state.move_piece(self.source, self.target)
        board_state.move_piece(self.__rook_source, self.__rook_target)

    def animate(self, current_frame: int) -> int:
        _animate_move(self.piece, self.target, current_frame)
        _animate_move(self.__rook_piece, self.__rook_target, current_frame)
        return FRAMES_PER_MOVE

    def __str__(self) -> str:
        return f"Castle {self.source} to {self.target}"
