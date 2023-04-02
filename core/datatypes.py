from dataclasses import dataclass



class Settings:
    def __init__(self, data: dict) -> None:
        self.name = data['game']['name']
        self.start_record = data['game']['replays']['start-record']
        self.end_record = data['game']['replays']['end-record']
        self.end_record = self.end_record if self.end_record != "None" else self.start_record

    def __repr__(self) -> str:
        return f'<Setting for "{self.name}" {self.end_record}>'