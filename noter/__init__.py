import argparse

from . import app


def main():

    # ihl ext -i img.jpg -o example.jpg -t TEXT -a center -s 50

    parser = argparse.ArgumentParser(
        description=f"Noter",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.set_defaults(func=app.run)
    parser.add_argument("-p", "--profile", default="default")

    arguments = parser.parse_args()
    arguments.func(arguments)

