import guick
import click
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# @guick.gui_option
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
@click.option("--flag", is_flag=True)
@click.option('--shout/--no-shout', default=True)
@click.option('--language', type=click.Choice(['c', 'c++']))
@click.option('-v', '--verbose', count=True)
def example_cmd(**argvs):
    for k, v in argvs.items():
        print(k, v, type(v))


@cli.command()
@click.option("--hello")
def sync(hello):
    print('Synching', hello)

class MyInt(click.types.ParamType):
    name = "my int"

    def convert(self, value, param, ctx):
        try:
            return int(value)
        except (ValueError, UnicodeError):
            self.fail('%s is not a valid integer' % value, param, ctx)

    @staticmethod
    def to_widget(opt):
        value = QLineEdit()
        value = QSlider(Qt.Horizontal)
        value.setMinimum(10)
        value.setMaximum(30)
        value.setValue(20)
        value.setTickPosition(QSlider.TicksBelow)
        value.setTickInterval(5)

        def to_command():
            return [opt.opts[0], str(value.value())]
        return [guick.generate_label(opt), value], to_command

@cli.command()
@click.option("--myint", type=MyInt(), help='my int')
def func(**argvs):
    print("==== running func")
    for k, v in argvs.items():
        print(k, v, type(v))

@guick.gui_option
@click.command()
def option_gui():
    """run with
    python test.py --gui
    """
    print("gui_option")


if __name__ == "__main__":
    # guick.gui_it(example_cmd, run_exit=True)
    # option_gui()
    guick.gui_it(cli, run_exit=False)
    # cli()
