from guick import gui_it
import click

@click.command()
@click.option("--hello", default="world", help="say hello")
@click.option("--add", type=int, help="input an integer number",\
              hide_input=True)
@click.option("--times", type=float, help="input a double number")
@click.option("--flag", is_flag=True)
@click.option('--shout/--no-shout', default=True)
@click.option('--language', type=click.Choice(['c', 'c++']))
@click.option('-v', '--verbose', count=True)
def example_cmd(**argvs):
    for k, v in argvs.items():
        print(k, v, type(v))


@click.group()
def cli():
    pass
# @click.option('--debug/--no-debug', default=False)
# def cli(debug):
    # print(debug)
    # click.echo('Debug mode is %s' % ('on' if debug else 'off'))

@cli.command()
@click.option("--hello")
def sync(hello):
    print('Synching', hello)

@cli.command()
def func():
    print("func")

if __name__ == "__main__":
    gui_it(example_cmd, run_exit=False)
    # gui_it(cli, run_exit=False)
