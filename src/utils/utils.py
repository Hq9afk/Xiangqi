import sys
import logging


def setup_console_logging():
    output_path = "match_results/match_results.log"
    logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[logging.FileHandler(output_path, encoding="utf-8"), logging.StreamHandler(sys.__stdout__)])

    class LoggerWriter:
        def write(self, message):
            if message.strip() != "":
                logging.info(message.strip())

        def flush(self):
            pass

    sys.stdout = LoggerWriter()
    sys.stderr = LoggerWriter()


def all_in_one_copy(original):
    if original is None:
        return None
    if isinstance(original, list):
        if not original:
            return []
        if isinstance(original[0], list) and original[0] and isinstance(original[0][0], str):
            # board type: list[list[str]]
            return [row[:] for row in original]
        elif isinstance(original[0], list) and original[0] and isinstance(original[0][0], tuple):
            # list of moves: list[list[tuple, tuple]]
            return [move[:] for move in original]
        elif isinstance(original[0], tuple):
            return original[:]  # shallow copy is enough
        else:
            return original[:]
    # Avoid direct reference to Move to keep utils decoupled
    if hasattr(original, "copy") and callable(original.copy):
        return original.copy()
    if isinstance(original, dict):
        return original.copy()
    return original
