import quick
import click
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# @quick.gui_option
@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    print(debug)


@cli.command()
@click.argument("arg", nargs=-1)
@click.option("--hello", default="world", help="say hello")
@click.option("--add", type=int, help="input an integer number",\
              hide_input=True)
@click.option("--times", type=float, default=2.3, help="input a double number")
@click.option("--minus", type=float, help="input two numbers", nargs=2)
@click.option("--tuple", type=(int, str), default=(23, 'quick'), help="input (int, str)", nargs=2)
@click.option("--flag", is_flag=True)
@click.option("--int_range", type=click.types.IntRange(10,20))
@click.option('--shout/--no-shout', default=True)
@click.option('--language', type=click.Choice(['c', 'c++']))
@click.option('-v', '--verbose', count=True)
def example_cmd(**argvs):
    for k, v in argvs.items():
        print(k, v, type(v))


class MyInt(click.types.ParamType):
    name = "my int range"

    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.help = "my int range"

    def convert(self, value, param, ctx):
        try:
            return int(value)
        except (ValueError, UnicodeError):
            self.fail('%s is not a valid integer' % value, param, ctx)

    def to_widget(self):
        value = QLineEdit()
        value = QSlider(Qt.Horizontal)
        value.setMinimum(self.min)
        value.setMaximum(self.max)
        value.setValue(self.min)
        value.setTickPosition(QSlider.TicksBelow)

        def to_command():
            return [self.opts[0], str(value.value())]
        return [quick.generate_label(self), value], to_command

@cli.command()
@click.option("--myint", type=click.IntRange(10, 20), help='my int')
def myint(**argvs):
    for k, v in argvs.items():
        print(k, v, type(v))

@cli.command()
@click.argument("default", type=click.Path(), nargs=-1)
@click.option("--file_path", type=click.Path(file_okay=True, dir_okay=False), help="select a file")
@click.option("--no_exist_path", type=click.Path(file_okay=False, dir_okay=False), help="select a file")
@click.option("--folders", type=click.Path(file_okay=False, dir_okay=True), nargs=3)
def pathtest(**argvs):
    for k, v in argvs.items():
        print(k, v, type(v))

@quick.gui_option
@click.command()
def option_gui():
    """run with
    python test.py --gui
    """
    print("gui_option")


if __name__ == "__main__":
    # quick.gui_it(example_cmd, run_exit=True)
    # option_gui()
    quick.gui_it(cli, run_exit=False)
    # cli()
