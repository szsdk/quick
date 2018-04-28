# QUICK

A real quick GUI generator for [click](https://github.com/pallets/click). Inspired by [Gooey](
https://github.com/chriskiehl/Gooey), the GUI generator for classical Python `argparse`-based command line programs.

## Install

```
python setup.py install
```

## Usage

### Overview
Open your terminal, go into the downloaded source folder and input
```python
python test.py
```
Then click "Run" button. You will see something like this.
<p align="center">
<img src="https://user-images.githubusercontent.com/6657200/38025934-bf93013c-32bc-11e8-8d12-91411b28946e.png" alt="screenshot" style="max-width:100%;" width="400">
</p>

Open `test.py` to see what the original click-based program looks like.

### Basic usage

This package could draw the gui for a click-based CLI program with a very
simple function `gui_it`. The usage is wrapping the command function
`example_cmd()`  like `gui_it(example_cmd)`. The full example is like
this.

```python
from quick import gui_it
import click

@click.command()
@click.option("--hello", default="world", help="say hello")
@click.option("--add", type=int, help="input an integer number",\
              hide_input=True)
@click.option("--minus", type=float, help="input two numbers", nargs=2)
@click.option("--flag", is_flag=True)
@click.option('--shout/--no-shout', default=True)
@click.option('--language', type=click.Choice(['c', 'c++']))
@click.option('-v', '--verbose', count=True)
def example_cmd(**argvs):
    for k, v in argvs.items():
        print(k, v, type(v))


if __name__ == "__main__":
    # example_cmd()
    gui_it(example_cmd)
```

###  Add `--gui` option to your command

A common case is not changing all your command into a gui version, but just
add a `--gui` option to it. Then you can do this.

```python
from quick import gui_option
import click

@gui_option
@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    print(debug)


@cli.command()
@click.argument("arg", nargs=-1)
@click.option("--hello", default="world", help="say hello")
@click.option('-v', '--verbose', count=True)
def example_cmd(**argvs):
    for k, v in argvs.items():
        print(k, v, type(v))


@cli.command()
@click.option("--hello")
def sync(hello):
    print('Synching', hello)


@cli.command()
def func(**argvs):
    pass

if __name__ == "__main__":
    cli()
```

### Writing you own widget


## For developer
Travis CI is used for continuous integration.

## Copyright
see LICENCE
