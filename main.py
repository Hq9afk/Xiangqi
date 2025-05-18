from src.game import Game as G
from src.utils.utils import setup_console_logging as log


def main():
    # Entry point for the Xiangqi game
    log()
    app = G()
    app.run()


if __name__ == "__main__":
    main()
