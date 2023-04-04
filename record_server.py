import sys
from core import utils
from pynput.mouse import Listener as MListener
from pynput.keyboard import Listener as KListener


def button(key):
    if key == 'q':
        quit(0)
        l.stop()
    print(key)


if __name__ == '__main__':
    path, folder = sys.argv
    games = utils.init_games()

    recording_game = games.dict[folder]
    
    key_to_start   = recording_game.start_record
    key_to_end     = recording_game.end_record
    keys_to_listen = recording_game.keys.split(',')

    l = KListener(button, button)
    l.start()
    l.join()
    

    print(keys_to_listen)