# Импорты
import os, yaml
import core.datatypes as cored

# Глобальные переменные
games: dict = {}



def init_games() -> None:
    "Инициализирует все папки в которых содержится файл game-settings.yaml"
    for element in os.listdir('.'):
        if os.path.isdir(element) and element != 'TemplateGame':
            for e in os.listdir(f'./{element}/'):
                if e == 'game-settings.yaml':
                    games[element] = parse_game_settings(f'./{element}/game-settings.yaml')


def parse_game_settings(path: str) -> 'cored.Settings':
    return cored.Settings(yaml.safe_load(open(path, 'r', encoding='utf8')))


def main() -> None:
    init_games()

if __name__ == '__main__':
    main()
    print(games)