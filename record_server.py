from core import utils
from pynput.mouse import Controller as MController
from pynput.keyboard import Controller as KController
from pynput import keyboard as Keyboard
import sys, time, copy



class KeyboardEvents():
    def __init__(self) -> None:
        self.list = []
    def add_event(self, event):
        self.list.append(event)
    def get_events(self):
        _ = copy.deepcopy(self.list)
        self.list = []

def keyboard_pressed(key):
    try:
        if key.char == 'q':
#            klistener.stop()
            quit(0)
    except Exception:
        pass
    keyboard_events.add_event(key)



if __name__ == '__main__':
    path, folder = sys.argv
    games = utils.init_games()
    keyboard_events = KeyboardEvents()

    recording_game = games.dict[folder]
    
    key_to_start   = recording_game.start_record
    key_to_end     = recording_game.end_record
    keys_to_listen = recording_game.keys.split(',')

    frame_delay = 1/15
"""    for i in range(10):
        for z in [1, 2, 3, 4]:
            with Keyboard.Events() as events:
                print(f'I: {i}, Z: {z}')
                
                print(list(events))
                #if events is not None:
                    #print([event for event in events])
                time.sleep(frame_delay)
                continue
"""
    mouse = MController()
    keyboard = KController()
    print(keys_to_listen)