# Импорты
import os, yaml
import core.datatypes as cored
import core.ui as coreui

# Глобальные переменные
games: 'cored.GamesList' = cored.GamesList()



def init_games() -> None:
    "Инициализирует все папки в которых содержится файл game-settings.yaml"
    for element in os.listdir('.'):
        if os.path.isdir(element) and element != 'TemplateGame':
            for e in os.listdir(f'./{element}/'):
                if e == 'game-settings.yaml':
                    game_settings = cored.Settings(yaml.safe_load(open(f'./{element}/game-settings.yaml', 'r', encoding='utf8')))
                    games.add_game(element, game_settings)


def main() -> None:
    init_games()
    print(games)
    coreui.start_ui(games)

if __name__ == '__main__':
    main()