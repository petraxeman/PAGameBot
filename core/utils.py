import os, shutil, yaml
import core.datatypes as cored


def init_games() -> 'cored.GamesList':
    "Инициализирует все папки в которых содержится файл game-settings.yaml"
    games = cored.GamesList()
    for element in os.listdir('.'):
        if os.path.isdir(element) and element != 'TemplateGame':
            for e in os.listdir(f'./{element}/'):
                if e == 'game-settings.yaml':
                    game_settings = cored.Settings(yaml.safe_load(open(f'./{element}/game-settings.yaml', 'r', encoding='utf8')))
                    games.add_game(element, game_settings)
    return games


def clone(folder_name: str):
    directories = os.listdir('./')
    index = 1
    while f'{folder_name} {index}' in directories:
        index += 1
    shutil.copytree(f'./{folder_name}', f'./{folder_name} {index}')

    settings = yaml.safe_load(open(f'./{folder_name} {index}/game-settings.yaml', 'r'))
    settings['name'] = f'{settings["name"]} {index}'
    yaml.safe_dump(settings, open(f'./{folder_name} {index}/game-settings.yaml', 'w'))


def delete(folder_name: str) -> None:
    shutil.rmtree(f'./{folder_name}')