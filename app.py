from data_explorer.canvas import Canvas
from src.settings import AppConfig


def main():

    parameters = AppConfig()

    canvas = Canvas(params=parameters)
    canvas.build()


if __name__ == "__main__":
    main()
