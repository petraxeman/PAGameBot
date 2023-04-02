# Импорты
from asciimatics.screen import ManagedScreen, Screen
from asciimatics.scene import Scene
from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, Button, TextBox, Widget
from time import sleep

# Глобальные переменные
#


class ChoiceGame(Frame):
    def __init__(self, screen, games_list: list) -> None:
        super().__init__(screen,
                         screen.height * 2 // 3,
                         screen.width * 2 // 3,
                         on_load=self._reload_list,
                         hover_focus=True,
                         can_scroll=False,
                         title='Choice Game')
        
        self.games_list = games_list

        self._list_view = ListBox(
            Widget.FILL_FRAME,
            games_list,
            name= 'Games',
            add_scroll_bar= True,
            on_change= self._on_pick,
            on_select= self._edit
        )
        self._create_new_button = Button('Create new', self._create_new)
        self._choice_button = Button('Choice', self._choice)
        self._exit_button = Button('Exit', self._exit)

        layout = Layout([100], fill_frame=True)
        layout2 = Layout([1, 1, 1])

        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        self.add_layout(layout2)
        layout2.add_widget(self._create_new_button, 0)
        layout2.add_widget(self._choice_button, 1)
        layout2.add_widget(self._exit_button, 2)
        self.fix()
    
    def _reload_list(self, new_value = None):
        self._list_view.options = self.games_list
        self._list_view.value = new_value
    
    def _on_pick(self,):
        self._choice_button.disabled = self._list_view.value is None

    def _edit(self,):
        pass

    def _create_new(self,):
        pass

    def _choice(self,):
        pass
    
    def _exit(self,):
        pass


def start_ui():
    with ManagedScreen() as screen:
        scenes = [
        Scene([ChoiceGame(screen, [['cdda', 'asd'],])], -1, name="Main"),
        #Scene([ContactView(screen, contacts)], -1, name="Edit Contact")
        ]
        screen.play(scenes, stop_on_resize=True, start_scene=None, allow_int=True)

start_ui()