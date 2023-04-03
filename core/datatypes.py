from dataclasses import dataclass



class Settings:
    def __init__(self, data: dict) -> None:
        self.name = data['name']
        self.start_record = data['replays']['start-record']
        self.fact_end_record = data['replays']['end-record']
        self.end_record = self.fact_end_record if self.fact_end_record != "None" else self.start_record

    def __repr__(self) -> str:
        return f'<Setting for "{self.name}" {self.end_record}>'


class GamesList:
    def __init__(self) -> None:
        self.dict = {}
        self.current = None#self.dict[list(self.dict.keys())[0]]

    def set_current(self, short_name: str = None, full_name: str = None) -> None:
        if short_name:
            self.current = self.dict[short_name]
        elif full_name:
            for sn in self.dict:
                if self.dict[sn].name == full_name:
                    self.current = self.dict[sn]
                    break
    
    def get_short_name(self, full_name: str) -> str:
        for short_name in self.dict:
            if self.dict[short_name].name == full_name:
                return short_name
        raise Exception(f'Not found {repr(full_name)}')

    def add_game(self, short_name: str, settings: 'Settings') -> None:
        self.dict[short_name] = settings
    
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