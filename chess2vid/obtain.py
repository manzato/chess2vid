
import chess.pgn


def get_game(file_name: str) -> chess.pgn.Game:
    with open(file_name) as fd:
        return chess.pgn.read_game(fd)
