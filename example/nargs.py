import quick
import click


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


if __name__ == "__main__":
    # quick.gui_it(example_cmd, run_exit=True)
    # option_gui()
    quick.gui_it(cli, run_exit=False, new_thread=False,
            style="qdarkstyle", width=450)
    # cli()
