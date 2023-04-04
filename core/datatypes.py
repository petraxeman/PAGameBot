from dataclasses import dataclass
import os, yaml


class Settings:
    def __init__(self, data: dict) -> None:
        self.folder_name = None
        self.name = data['name']
        self.keys = data['keys']
        self.start_record = data['replays']['start-record']
        self.fact_end_record = data['replays']['end-record']
        self.end_record = self.fact_end_record if self.fact_end_record != "None" else self.start_record
        
        self.resolution_type = data['replays']['resolution']['type']
        self.text_resolution = data['replays']['resolution']['fact']
        self.resolution = self.build_resolution(self.text_resolution) if self.resolution_type == 'custom' \
                                                                    else self.build_resolution(self.resolution_type)

        self.filtering = data['replays']['formating']['filtering']
        self.threshold = data['replays']['formating']['opencv_threshold']
        self.blur = data['replays']['formating']['opencv_blur']
        self.threshold = int(self.threshold) if self.threshold != 'None' else None
        self.blur = int(self.blur) if self.blur != 'None' else None

    def build_resolution(self, string: str) -> tuple:
        x, y = string.split('x')
        return (int(x), int(y))
    
    def build_yaml(self, file) -> None:
        data = {'name' : self.name,
                'keys' : self.keys,
                'replays': {
                    'start-record' : self.start_record,
                    'end-record' : self.fact_end_record,
                    'resolution' : {
                        'type' : self.resolution_type,
                        'fact' : self.text_resolution,
                    },
                    'formating' : {
                        'filtering' : self.filtering,
                        'opencv_threshold' : self.threshold,
                        'opencv_blur' : self.blur
                    }
                }}
        yaml.safe_dump(data, file)

    def __repr__(self) -> str:
        return f'<Setting for "{self.name}" {self.end_record}>'
    
    @classmethod
    def create_empty(cls):
        data = {'name' : 'Undefined',
                'keys' : 'w,a,s,d',
                'replays': {
                    'start-record' : 'l',
                    'end-record' : 'None',
                    'resolution' : {
                        'type' : '16x9',
                        'fact' : '16x9',},
                    'formating' : {
                        'filtering' : 'True',
                        'opencv_threshold' : '120',
                        'opencv_blur' : '7'}}}
        return cls(data)



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