import json

import pytermgui as ptg
import requests


with ptg.YamlLoader() as loader, open('config.yaml', 'r') as yaml_file:
    namespace = loader.load(yaml_file)


class InputWindow:
    manager: ptg.WindowManager
    window: ptg.Window

    close_button: ptg.Button
    url_input: ptg.InputField

    warning_label: ptg.Label

    def __init__(self, manager):
        self.manager = manager
        self.setup_window()
        self.results_window = OurCustomWindow(self)

    def setup_window(self):
        self.window = namespace.InputBox.center()

        self.close_button = ptg.get_widget('get-data-button')
        self.url_input = ptg.get_widget('input-field')
        self.close_button.onclick = lambda *_: self.update_windows()
        self.warning_label = ptg.get_widget('warning-label')

    def update_windows(self):
        if self.url_input.value == 'test':
            url_text = 'https://jsonplaceholder.typicode.com/todos/1'
        else:
            url_text = self.url_input.value

        try:
            string = requests.get(url_text).json()
        except requests.exceptions.MissingSchema:
            self.warning_label.value = 'Error: Invalid URL.'
        else:
            self.warning_label.value = f'Fetching {url_text}'
            self.results_window = OurCustomWindow(self)
            self.results_window.set_text(json.dumps(string), json.dumps(string, indent=2))
            self.manager.add(self.results_window.window)
            self.window.close()

    def open(self):
        del self.window
        self.setup_window()
        self.manager.add(self.window)


class OurCustomWindow:
    parent: InputWindow
    window: ptg.Window

    left_box: ptg.Container
    right_box: ptg.Container

    left_label: ptg.Label
    right_label: ptg.Label

    close_button: ptg.Button

    def __init__(self, parent):
        self.parent = parent

        self.setup_window()

    def setup_window(self):
        self.window = namespace.SplitBox.center()
        self.left_box = ptg.get_widget('left-box')
        self.right_box = ptg.get_widget('right-box')

        self.left_label = ptg.get_widget('left-label')
        self.right_label = ptg.get_widget('right-label')

        self.close_button = ptg.get_widget('close-button')
        self.close_button.onclick = lambda *_: self.handle_close()

    def handle_close(self):
        self.window.close()
        self.parent.open()

    def set_text(self, raw_string, processed_string):
        self.left_label.value = raw_string
        self.right_label.value = processed_string
        self.window.is_dirty = True
