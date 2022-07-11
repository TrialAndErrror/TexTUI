import pytermgui as ptg

from src.models import InputWindow


def main():
    with ptg.WindowManager() as manager:
        window = InputWindow(manager)
        manager.add(window.window)
        manager.run()


if __name__ == '__main__':
    main()



