from core import utils
import os, yaml


class Settings:
    def __init__(self, data: dict, folder: str) -> None:
        # БАЗОВЫЕ ПАРАМЕТРЫ
        self.folder_name: str          = folder
        self.name: str                 = data['base']['name']
        
        # ПАРАМЕТРЫ РЕПЛЕЯ
        self.start_record: str         = data['replays']['start-record']
        self.end_record: str           = data['replays']['end-record']
        self.text_end_record: str      = data['replays']['end-record']
        self.decline_record: str       = data['replays']['decline-record']
        self.listening_keys: list[str] = data['replays']['listening-keys'].split(',')
        self.process_when_record: bool = bool(data['replays']['process-when-record'])
        self.framerate: int            = int(data['replays']['frame-rate'])
        self.resolution_type: str      = data['replays']['resolution']['type']
        self.resolution_fact: str      = data['replays']['resolution']['fact']
        self.resolution_size: int      = int(data['replays']['resolution']['size'])

        # ПАРАМЕТРЫ РЕДАКТИРОВАНИЯ ИЗОБРАЖЕНИЯ
        self.algorithm: str            = data['image-editing']['algorithm']

        self.contours_threshold: int   = int(data['image-editing']['contours']['threshold'])
        self.contours_blur: int        = int(data['image-editing']['contours']['blur'])

        self.canny_min_threshold: int  = int(data['image-editing']['canny']['min-threshold'])
        self.canny_max_threshold: int  = int(data['image-editing']['canny']['max-threshold'])

        self.fix_values()
    
    def fix_values(self) -> None:
        self.end_record = self.end_record if self.end_record != "None" else self.start_record

    def get_size(self) -> tuple[int]:
        w, h = self.resolution_fact.split('x')
        w, h = int(w), int(h)
        step = self.resolution_size // (w + h) 
        return step * w, step * h
    
    def build_yaml(self, file) -> None:
        data = utils.build_dict_from_settings(self)
        yaml.safe_dump(data, file)

    def __repr__(self) -> str:
        return f'<Setting for "{self.name}">'
    
    @classmethod
    def create_empty(cls) -> 'Settings':
        data = yaml.safe_load('./TemplateGame/game-settings.yaml')
        data['base']['name'] = 'Untitled'
        return cls(data, None)



class GamesList:
    def __init__(self) -> None:
        self.dict = {}
        self.current = None

    def set_current(self, short_name: str = None, full_name: str = None) -> None:
        if short_name:
            self.current = self.dict[short_name]
        elif full_name:
            for sn in self.dict:
                if self.dict[sn].name == full_name:
                    self.current = self.dict[sn]
                    break
        else:
            self.current = None
    
    def get_short_name(self, full_name: str) -> str:
        for short_name in self.dict:
            if self.dict[short_name].name == full_name:
                return short_name
        raise Exception(f'Not found {repr(full_name)}')

    def add_game(self, short_name: str, settings: 'Settings') -> None:
        settings.folder_name = short_name
        self.dict[short_name] = settings
    
    def update_notes(self) -> None:
        for element in os.listdir('.'):
            if os.path.isdir(element) and element != 'TemplateGame':
                if 'game-settings.yaml' in os.listdir(f'./{element}/'):
                    game_settings = Settings(yaml.safe_load(open(f'./{element}/game-settings.yaml', 'r', encoding='utf8')))
                    self.add_game(element, game_settings)
        
        exist_dirs = os.listdir('./')
        for key in list(self.dict.keys()):
            if key not in exist_dirs:
                del self.dict[key]
            

    def get_summary(self) -> list[tuple]:
        summary = []
        index = 0
        for short_name in self.dict:
            if short_name == 'temp':
                continue
            summary.append((self.dict[short_name].name, index))
            index += 1
        return summary
    
    def __repr__(self) -> str:
        return f'<Games list now contains {len(self.dict)} games>'