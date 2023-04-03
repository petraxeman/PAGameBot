# Импорты
import os, yaml
import core.datatypes as cored
import core.ui as coreui
import core.utils as utils



def main() -> None:
    games = utils.init_games()
    coreui.start_ui(games)

if __name__ == '__main__':
    main()