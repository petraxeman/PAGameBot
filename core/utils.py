import os, shutil, yaml
import core.datatypes as cored


def init_games() -> 'cored.GamesList':
    "Инициализирует все папки в которых содержится файл game-settings.yaml"
    games = cored.GamesList()
    for element in os.listdir('.'):
        if os.path.isdir(element) and element != 'TemplateGame':
            for e in os.listdir(f'./{element}/'):
                if e == 'game-settings.yaml':
                    game_settings = cored.Settings(yaml.safe_load(open(f'./{element}/game-settings.yaml', 'r', encoding='utf8')), element)
                    games.add_game(element, game_settings)
    return games


def clone(folder_name: str):
    "Клонирование директории"
    directories = os.listdir('./')
    index = 1
    while f'{folder_name} {index}' in directories:
        index += 1
    shutil.copytree(f'./{folder_name}', f'./{folder_name} {index}')

    settings = yaml.safe_load(open(f'./{folder_name} {index}/game-settings.yaml', 'r'))
    settings['name'] = f'{settings["name"]} {index}'
    yaml.safe_dump(settings, open(f'./{folder_name} {index}/game-settings.yaml', 'w'))


def build_dict_from_settings(self, settings) -> dict:
    data = {'base': 
                {'name' : settings.name},
            'replays': {
                'start-record'   : settings.start_record,
                'end-record'     : settings.text_end_record,
                'decline-record' : settings.decline_record,
                'listenig_keys'  : string_from_list(settings.listening_keys),
                'resolution' : {
                    'type'       : settings.resolution_type,
                    'fact'       : settings.resolution_fact,
                    'size'       : settings.resolution_size,
                },
                'formating' : {
                    'filtering' : settings.filtering,
                    'opencv_threshold' : settings.threshold,
                    'opencv_blur' : settings.blur
                }
            }}


def string_from_list(elements: list[str]) -> str:
    string = ''
    for element in elements:
        string += element + ','
    return string


def delete(folder_name: str) -> None:
    shutil.rmtree(f'./{folder_name}')