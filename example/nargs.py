import quick
import click

@quick.gui_option(run_exit=False, new_thread=False, output="gui", style="qdarkstyle", width=450, top=45)
@click.group(help="Test for quick library")
@click.option('--debug/--no-debug', default=False)
def cli(**argvs):
    for k, v in argvs.items():
        print(k, v, type(v))

@cli.command()
@click.argument("multiarg", nargs=-1)
def norequire(multiarg):
    print(multiarg)

@cli.command()
@click.argument("multiarg", nargs=-1, required=True)
def require(multiarg):
    print("run:", multiarg)

@cli.command()
def error():
    raise Exception("error")

@cli.command()
@click.argument("arg", nargs=1, type=click.Choice(['c', 'c++']))
def argument(arg, *argvs):
    print(arg)
    # for k, v in argvs.items():
        # print(k, v, type(v))

if __name__ == "__main__":
    # quick.gui_it(example_cmd, run_exit=True)
    # option_gui()
    # quick.gui_it(cli, run_exit=False, new_thread=False, output="gui",
    #         style="qdarkstyle", width=450, top=45)
    cli()
