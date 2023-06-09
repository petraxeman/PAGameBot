from pynput.keyboard import Listener as KListener
from pynput.keyboard import Key
from pynput.mouse import Controller as MController
from pynput.mouse import Listener as MListener
from pynput.mouse import Button
from core import utils
from datetime import datetime
import sys, time, os, mss, cv2, shutil, dxcam
import numpy as np

#bounding_box = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
#sct = mss.mss()
previous_image = None
camera = dxcam.create(device_idx=0, output_color='BGRA')

keymap: dict = dict()
key_specials: dict = {Key.alt: 'alt', Key.alt_gr: 'alt', Key.alt_l: 'alt', Key.alt_r: 'alt',
                      Key.ctrl: 'ctrl', Key.ctrl_l: 'ctrl', Key.ctrl_r: 'ctrl',
                      Key.shift: 'shift', Key.shift_l: 'shift', Key.shift_r: 'shift',
                      Key.caps_lock: 'caps-lock', Key.tab: 'tab', Key.space: 'space',
                      Key.cmd: 'cmd', Key.cmd_l: 'cmd', Key.ctrl_r: 'cmd',
                      Key.esc: 'esc', Key.enter: 'enter'}
key_specials_list: list = list(key_specials.keys())
possible_keys: list = list()

mousemap: dict = {'lmb': False, 'rmb': False, 'scroll': 0, 'move': (0, 0)}
mouse_buttons: dict = {Button.left: 'lmb', Button.right: 'rmb'}
mouse_prev_pos: tuple = (0, 0)

program_close = False
recording = False
delete_current_record = False



def on_press(key: 'Key') -> None:
    global keymap, program_close, recording, delete_current_record
    if 'char' in dir(key):
        if key.char in possible_keys:
            keymap[key.char] = True
        if key.char in [key_to_start, key_to_end, key_to_decline]:
            if key.char == key_to_start and not recording:
                recording = True
            elif key.char == key_to_end and recording:
                recording = False
            elif key.char == key_to_decline and recording:
                recording = False
                delete_current_record = True
    else:
        if key == Key.esc:
            program_close = True
            recording = False
            klistener.stop()
            mlistener.stop()
        if key in key_specials_list and key_specials[key] in possible_keys:
            keymap[key_specials[key]] = True


def on_release(key: 'Key') -> None:
    global keymap
    if 'char' in dir(key) and key.char in possible_keys:
        keymap[key.char] = False
    else:
        if key in key_specials_list and key_specials[key] in possible_keys:
            keymap[key_specials[key]] = False


def on_click(x, y, button, is_pressed) -> None:
    global mousemap
    if is_pressed:
        mousemap[mouse_buttons[button]] = True


def on_scroll(x, y, dx, dy) -> None:
    global mousemap
    if dy < 0:
        mousemap['scroll'] = -1
    elif dy > 0:
        mousemap['scroll'] = 1


def on_move() -> None:
    global mousemap, mouse_prev_pos
    x = mouse_prev_pos[0] - mcontroller.position[0]
    y = mouse_prev_pos[1] - mcontroller.position[1]
    mousemap['move'] = (x, y)
    mouse_prev_pos = mcontroller.position


def end_input() -> None:
    global mousemap
    mousemap['lmb'] = False
    mousemap['rmb'] = False
    mousemap['scroll'] = 0


def build_keymap(keys: list) -> None:
    global keymap, possible_keys
    for key in keys:
        key = key.strip()
        keymap[key] = False
        possible_keys.append(key)


def write_head(file) -> None:
    head = 'frame_id '
    for key in possible_keys:
        head += key + ' '
    head += 'mouse_lmb mouse_rmb mouse_scroll mouse_move'
    file.write(head + '\n')


def record_input(file, frame_id: int) -> None:
    line = str(frame_id) + ' '
    for key in possible_keys:
        line += str(int(keymap[key])) + ' '
    line += str(int(mousemap['lmb'])) + ' '
    line += str(int(mousemap['rmb'])) + ' '
    line += str(mousemap['scroll']) + ' '
    line += str(mousemap['move'])
    file.write(line + '\n')


def record_screen(path: str, frame_id: int) -> None:
    global camera, previous_image, resolution
    image = camera.grab()
    if image is not None:
        image_to_write = image
        previous_image = image
    else:
        image_to_write = previous_image
    #image_to_write = np.array(image_to_write)
    image_to_write = cv2.resize(image_to_write, resolution)
    cv2.imwrite(f'{path}/Frame-{frame_id}.png', image_to_write)


def record(folder: str) -> None:
    global recording, keymap, mousemap, camera
    delay = 1 / recording_game.framerate
    frame_id = 0

    current_time = datetime.now()
    current_time = current_time.strftime('%d.%m.%Y %H.%M')
    timestamp_hash = hash(datetime.now().timestamp)
    path_to_replay = f'./{folder}/replays/Replay at {current_time} - {timestamp_hash}'
    os.mkdir(path_to_replay)
    input_data = open(f'{path_to_replay}/input_data.csv', 'w', encoding='utf8')
    write_head(input_data)
    
    print('Replay recording')

    
    start_time = datetime.now().timestamp()
    while recording:
        frame_id += 1
        on_move()
        record_input(input_data, frame_id)
        record_screen(path_to_replay, frame_id)
        end_input()
        time.sleep(delay)
    end_time = datetime.now().timestamp()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output = cv2.VideoWriter(f'{path_to_replay}/video.mp4', fourcc, 15.0, resolution)
    for index in range(frame_id):
        index += 1
        frame = cv2.imread(f'{path_to_replay}/Frame-{index}.png')
        output.write(frame)
    output.release()
    input_data.close()

    if delete_current_record:
        print("Replay declined!")
        shutil.rmtree(path_to_replay)
    else:
        print(f'Replay saved at "{path_to_replay}')
        print(f'Recorded: {round(end_time-start_time, 2)}s')
        print(f'Frames count: {frame_id}')
        print(f'Approximate frame rate: {round(frame_id / (end_time-start_time), 2)}')


if __name__ == '__main__':
    path, folder = sys.argv
    games = utils.init_games()
    
    recording_game = games.dict[folder]
    resolution = recording_game.get_size()

    key_to_start: str   = recording_game.start_record
    key_to_end: str     = recording_game.end_record
    key_to_decline: str = recording_game.decline_record
    build_keymap(recording_game.listening_keys)

    klistener: 'KListener'     = KListener(on_press=on_press, on_release=on_release)
    mlistener: 'MListener'     = MListener(on_click=on_click, on_scroll=on_scroll)
    mcontroller: 'MController' = MController()

    klistener.start()
    mlistener.start()

    while not program_close:
        if recording:
            record(folder)