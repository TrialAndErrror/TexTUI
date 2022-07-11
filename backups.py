import json

import pytermgui as ptg
import requests


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
