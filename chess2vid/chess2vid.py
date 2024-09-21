import os
import bpy
from multiprocessing import Pool

from chess import (
    BLACK,
    SQUARES,
    WHITE,
    Board,
    Color,
    Move,
    Square,
)
import chess.pgn

from chess.pgn import Game

from chess2vid.actions import (
    Action,
    CastleAction,
    DrawSquareAction,
    MoveAction,
    PlacePieceAction,
    TakeAction,
)
from chess2vid.animator import Animator
from chess2vid.blender import create_camera, create_light, create_material
from chess2vid.board_state import BoardState
from chess2vid.exceptions import NoPieceError
from chess2vid.piece_factory import StlPieceFactory

from chess2vid.material import set_light_material, set_dark_material


def get_game(file_name: str) -> Game:
    with open(file_name) as fd:
        return chess.pgn.read_game(fd)


def square_color(square: Square) -> Color:
    base = square & 0x01 == 0x01
    invert = square & 0x08 == 0x08

    if base:
        return BLACK if invert else WHITE
    else:
        return WHITE if invert else BLACK


def _get_action_from_move(board: Board, board_state: BoardState, move: Move) -> Action:
    target_occupant = board_state.get_piece_or_none(move.to_square)

    try:
        piece = board_state.get_piece(move.from_square)
    except ValueError:
        print(move)
        raise

    if board.is_castling(move):
        return CastleAction(move.from_square, move.to_square, piece)

    if target_occupant:
        return TakeAction(move.from_square, move.to_square, piece, move.promotion)
    else:
        return MoveAction(move.from_square, move.to_square, piece, move.promotion)


class Chess2Vid:

    def __init__(
        self,
        frame_width: int,
        frame_height: int,
        input_game: str,
        output_path: str,
        stl_path: str,
        verbose: bool,
    ):
        self.__frame_width = frame_width
        self.__frame_height = frame_height
        self.__output_path = output_path
        self.__stl_path = stl_path
        self.__verbose = verbose

        # Start with an empty world (no camera, lights, etc)
        bpy.ops.wm.read_factory_settings(use_empty=True)

        set_light_material(create_material("white", [1, 1, 1, 1]))
        set_dark_material(create_material("black", [0, 0, 0, 1]))

        self.__game: Game = get_game(file_name=input_game)

    def verbose(self, str):
        if self.__verbose:
            print(str)

    def create_frames(self) -> bool:
        self.verbose("Creating cameras")

        (camera, camera_target) = create_camera()
        create_light()

        piece_factory = StlPieceFactory(self.__stl_path)
        board_state = BoardState()
        actions: list[Action] = []

        self.verbose("Generating square actions")

        for square in SQUARES:
            color = square_color(square)
            action = DrawSquareAction(square, color)

            self.verbose(f"Applying action {action}")
            action.apply(board_state)
            actions.append(action)

        self.verbose("Placing pieces")
        board = self.__game.board()
        for square, piece in board.piece_map().items():
            action = PlacePieceAction(
                square, piece.piece_type, piece.color, piece_factory
            )
            self.verbose(f"Applying action {action}")
            action.apply(board_state)
            actions.append(action)

        # Reset the board to its initial state (will one by one apply the moves so that the
        # state of the board mutates along with the moves as we traverse the game)
        board.reset_board()

        self.verbose(board.board_fen())
        for move in self.__game.mainline_moves():
            try:
                action = _get_action_from_move(board, board_state, move)
            except NoPieceError:
                print(f"Failed to process move {move}")
                return False

            self.verbose(f"#{board.fullmove_number} Applying action {action}")
            try:
                action.apply(board_state)
            except NoPieceError:
                print(
                    f"Failed to apply action {action}, #{board.fullmove_number} {move}"
                )
                return False

            board.push(move)
            actions.append(action)
            self.verbose(board.board_fen())

        animator = Animator(self.__verbose)

        camera.keyframe_insert("location", frame=1)

        for action in actions:
            self.verbose(f"Animate {action}")
            try:
                animator.animateAction(action)
            except AttributeError as e:
                print(f"Failed to animate {action}")
                raise e from None

        camera.location.x = 8
        camera.location.y = 6
        camera.location.y = 3
        camera.keyframe_insert("location", frame=animator.get_total_frames())

        return True

    def render_frames(self, start: int | None, end: int | None):
        scene = bpy.context.scene
        scene.render.resolution_x = self.__frame_width
        scene.render.resolution_y = self.__frame_height

        if not end:
            end = bpy.context.scene.frame_end

        print(f"Rendering frames from {start} to {end}")

        print(f"Number of CPUs available: {os.cpu_count()}")
        pool = Pool(processes=os.cpu_count())

        pool.map(self.render_frame, range(start, end + 1))

        pool.close()
        pool.join()


    def render_frame(self, frame):
        scene = bpy.context.scene
        print(f"Rendering frame {frame}!")
        scene.frame_current = frame
        scene.render.filepath = os.path.join(
            self.__output_path, f"{str(frame)}.png"
        )
        bpy.ops.render.render(write_still=True)
