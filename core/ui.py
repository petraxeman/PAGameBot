# Импорты
from asciimatics.screen import ManagedScreen, Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, Button, \
    RadioButtons, TextBox, Widget, DropdownList, Label
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
from time import sleep
from core import utils, datatypes
import sys, os

# Глобальные переменные
#

# UI Code
class MainMenu(Frame):
    def __init__(self, screen) -> None:
        super().__init__(screen,
                    screen.height * 2 // 3,
                    screen.width * 2 // 3,
                    on_load=self._filtering_replace_callback,
                    hover_focus=True,
                    can_scroll=False,
                    title='Main menu')
        
        layout = Layout([100], fill_frame = True)
        self.add_layout(layout)
        layout.add_widget(Button("Game manager", self._game_manager_callback), 0)
        layout.add_widget(Button("Filter replays", self._filtering_replace_callback), 0)
        layout.add_widget(Button("Start record server", self._start_record_server_callback), 0)
        layout.add_widget(Button('Quit', self._quit), 0)
        self.fix()
    
    def _game_manager_callback(self) -> None:
        raise NextScene("GameManager")

    def _filtering_replace_callback(self) -> None:
        pass

    def _start_record_server_callback(self) -> None:
        pass
    
    def _quit(self) -> None:
        raise StopApplication("User pressed quit")


class GameManager(Frame):
    def __init__(self, screen, games_list) -> None:
        super().__init__(screen,
                         screen.height * 2 // 3,
                         screen.width * 2 // 3,
                         on_load=self._reload_list,
                         hover_focus=True,
                         can_scroll=False,
                         title='Game manager')
        
        self.games_list = games_list

        self.list_view = ListBox(
            Widget.FILL_FRAME,
            games_list.get_summary(),
            name = 'games',
            add_scroll_bar = True,
            on_change = self._on_pick,
            on_select = self._select
        )

        self._select_button = Button('Select', self._select)
        layout = Layout([100], fill_frame=True)
        layout2 = Layout([1, 1, 1, 1])

        self.add_layout(layout)
        layout.add_widget(self.list_view)
        layout.add_widget(Divider())

        self.add_layout(layout2)
        layout2.add_widget(Button('Create new', self._create_new), 0)
        layout2.add_widget(Button('Clone', self._clone), 1)
        layout2.add_widget(self._select_button, 2)
        layout2.add_widget(Button('Back', self._back), 3)
        
        self.fix()
    
    def _reload_list(self, new_value = None):
        self.games_list.update_notes()
        self.list_view.options = self.games_list.get_summary()
        self.list_view.value = new_value
    
    def _on_pick(self,):
        self._select_button.disabled = self.list_view.value is None

    def _select(self,):
        self.save()
        self.games_list.set_current(full_name = self.list_view.options[self.list_view.value][0])
        raise NextScene('GameView')

    def _create_new(self,):
        self.games_list.current = datatypes.Settings.create_empty()
        raise NextScene("GameView")
    
    def _clone(self,):
        utils.clone(self.games_list.get_short_name(self.list_view.options[self.list_view.value][0]))
        self._reload_list()

    def _back(self,):
        raise NextScene('MainMenu')


class GameView(Frame):
    def __init__(self, screen, games_list):
        super().__init__(screen,
                         screen.height * 2 // 3,
                         screen.width * 2 // 3,
                         on_load=self._on_load,
                         hover_focus=True,
                         can_scroll=False,
                         title='Game View')

        self.games_list = games_list
        self.is_new = False
        
        layout_1l = Layout([100])
        layout_2l = Layout([1, 1])
        layout_3l = Layout([100])
        layout_el = Layout([1, 1, 1, 1], fill_frame=True)

        self.folder_name = Text("Folder name:", "folder_name")
        self.name_field = Text('Name:', 'name')
        self.keys_listening = Text('Keys:', 'keys')
        
        self.start_record = Text('Start record:', 'startrecordkey', max_length=4)
        self.end_record = Text('End record:', 'endrecordkey', max_length=4)

        self.resolution_type = DropdownList([('16x9', 0), ('4x3', 1), ('custom', 2)], 'Resolution preset:', on_change=self._resolution_changed)
        self.resolution_fact = Text('Resolution:', 'resolution')
        self.filtering = RadioButtons([('On', 0), ('Off', 1)], 'Filtering', on_change=self._filtering_change)
        self.threshold = Text('Threshold:', 'threshold', max_length=4)
        self.blur = Text('Blur:', 'blur', max_length=4)

        self.delete_button = Button('Delete', self._delete)

        self.add_layout(layout_1l)
        self.add_layout(layout_2l)
        self.add_layout(layout_3l)
        self.add_layout(layout_el)

        layout_1l.add_widget(Label('Main settings', height=2))
        layout_1l.add_widget(self.folder_name)
        layout_1l.add_widget(self.name_field)
        layout_1l.add_widget(self.keys_listening)

        layout_2l.add_widget(self.start_record, 0)
        layout_2l.add_widget(self.end_record, 1)
        layout_2l.add_widget(Divider())

        layout_3l.add_widget(Label('Replay settings', height=2))
        layout_3l.add_widget(self.resolution_type)
        layout_3l.add_widget(self.resolution_fact)
        layout_3l.add_widget(self.filtering)
        layout_3l.add_widget(self.threshold)
        layout_3l.add_widget(self.blur)
        layout_3l.add_widget(Divider())

        layout_el.add_widget(self.delete_button, 0)
        layout_el.add_widget(Button('Save', self._save), 2)
        layout_el.add_widget(Button('Back', self._back), 3)
        
        self.fix()
    
    def reset(self,) -> None:
        super(GameView, self).reset()
    
    def _on_load(self,) -> None:
        if self.games_list.current is None:
            self.delete_button.disabled = True
            self.folder_name.disabled = False
            self.is_new = True
            return
        elif self.games_list.current.folder_name is None:
            self.delete_button.disabled = True
            self.folder_name.disabled = False
            self.is_new = True
        else:
            self.delete_button.disabled = False
            self.folder_name.disabled = True
            self.is_new = False
        
        self.current = self.games_list.current
        self.title = f'{self.current.name} view'
        
        self.folder_name.value = self.current.folder_name
        self.name_field.value = self.current.name
        self.keys_listening.value = self.current.keys

        self.start_record.value = self.current.start_record
        self.end_record.value = self.current.fact_end_record

        resdict = {'16x9': 0, '4x3': 1, 'custom': 2}
        self.resolution_type.value = resdict[self.current.resolution_type]
        self.resolution_fact.value = self.current.text_resolution

        self.filtering.value = (int(bool(self.current.filtering)) - 1) * -1
        self.threshold.value = str(self.current.threshold)
        self.blur.value = str(self.current.blur)

    def _resolution_changed(self) -> None:
        value = self.resolution_type.value
        if self.resolution_type.options[value][0] != 'custom':
            self.resolution_fact.value = self.resolution_type.options[value][0]
            self.resolution_fact.disabled = True
        else:
            self.resolution_fact.disabled = False

    def _filtering_change(self) -> None:
        if self.filtering.value == 1:
            self.threshold.disabled = True
            self.blur.disabled = True
        else:
            self.threshold.disabled = False
            self.blur.disabled = False

    def _delete(self,) -> None:
        utils.delete(self.games_list.get_short_name(self.name_field.value))
        raise NextScene("GameManager")
    
    def _save(self,) -> None:
        if self.folder_name.value in os.listdir('./') and self.is_new:
            return
        
        if self.is_new:
            os.mkdir(f'./{self.folder_name.value}')

        self.current.name = self.name_field.value
        self.current.keys = self.keys_listening.value
        self.current.start_record = self.start_record.value
        self.current.fact_end_record = self.end_record.value

        self.current.resolution_type = self.resolution_type.options[self.resolution_type.value][0]
        self.current.text_resolution = self.resolution_fact.value

        a = self.filtering._options[self.filtering.value][1] - 1
        self.current.filtering = bool(a)
        self.current.threshold = self.threshold.value if self.threshold.value != '' else 'None'
        self.current.blur = self.blur.value if self.blur.value != '' else 'None'

        with open(f'./{self.folder_name.value}/game-settings.yaml', 'w', encoding='utf8') as file:
            self.current.build_yaml(file)

        raise NextScene("GameManager")

    def _back(self,) -> None:
        raise NextScene("GameManager")

    
def start_ui(games_list):
    last_scene = None
    with ManagedScreen() as screen:
        while True:
            try:
                scenes = [
                    Scene([MainMenu(screen)], -1, name = "MainMenu"),
                    Scene([GameManager(screen, games_list)], -1, name="GameManager"),
                    Scene([GameView(screen, games_list)], -1, name="GameView"),
                ]
                screen.play(scenes, stop_on_resize=True, start_scene=last_scene, allow_int=True)
                sys.exit(0)
            except ResizeScreenError as e:
                last_scene = e.scene