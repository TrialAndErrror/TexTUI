from src.docs import print_docs
import pytermgui as ptg
from pytermgui import tim, pretty
import requests
import json


def show_text_in_window(text_lines, manager):
    window = ptg.Window(
        "[wm-title]My first window!",
        *text_lines,
        ["Exit", lambda *_: manager.stop()],
    )

    return window


def define_layout() -> ptg.Layout:
    layout = ptg.Layout()

    layout.add_slot("Header", height=1)
    layout.add_break()
    return layout


def make_api_fetch_window() -> ptg.Window:
    demo = ptg.Window(
        ptg.Label("[210 bold]Enter API URL:"),
        ptg.Label(),
        ptg.InputField(prompt="Who are you?"),
        ptg.Label(),
        ptg.Button("Submit!")
    )

    return demo


def get_text() -> str:
    return requests.get('https://jsonplaceholder.typicode.com/todos/1').json()
    # return requests.get('https://jsonplaceholder.typicode.com/todos/1').content


def yaml_window(manager):
    loader = ptg.YamlLoader()

    with open('config.yaml', 'r') as yaml_file:
        namespace = loader.load(yaml_file)

    manager.layout = define_layout()
    manager.add(namespace.MainWindow.center())

    button = ptg.get_widget("button-close")
    button2 = ptg.get_widget("button-definition")


    """
        container 1 add json.dumps(raw.json())
        container 2 add 
    """
    string = get_text()
    demo = ptg.Window(
        ptg.Label(json.dumps(string)),
        ptg.Label(json.dumps(string, indent=2)),
        ptg.InputField(prompt="Who are you?"),
        ptg.Label(),
        ptg.Button("Submit!")
    )

    button2.onclick = lambda *_: manager.add(demo)

    button.onclick = lambda *_: manager.stop()

    return manager


class InputWindow:
    manager: ptg.WindowManager
    window: ptg.Window

    def __init__(self, manager):
        self.manager = manager
        self.setup_window()

        self.left_window = OurCustomWindow(manager, 'left-label')
        self.right_window = OurCustomWindow(manager, 'right-label')

    def setup_window(self):
        self.window = ptg.Window(
            ptg.Label('Enter API Url'),
            ptg.InputField('URL', id='input-field'),
            ptg.Button("Get Data", id='get-data-button')
        )

        button = ptg.get_widget('get-data-button')
        input_field = ptg.get_widget('input-field')
        button.onclick(lambda _: self.update_windows(input_field.value))

    def update_windows(self, text):
        string = requests.get(text).json()
        self.left_window.set_text(json.dumps(string))
        self.right_window.set_text(json.dumps(string, input=2))

        self.manager.add(self.left_window.window)
        self.manager.add(self.right_window.window)


class OurCustomWindow:
    manager: ptg.WindowManager
    window: ptg.Window
    label: ptg.Label

    def __init__(self, manager, label_id):
        self.manager = manager
        self.window = ptg.Window()
        self.label_id = label_id

    def setup_window(self):
        self.window = ptg.Window(
            ptg.Label('', id=self.label_id),
            ptg.Label(),
            ptg.Button("Close", id='close-button')
        )

        self.label = ptg.get_widget(self.label_id)

    def set_text(self, string):
        self.label.value = string


def main():
    with ptg.WindowManager() as manager:
        manager = yaml_window(manager)
        manager.run()


if __name__ == '__main__':
    main()



