import quick
import click


@click.group()
@click.option("--debug/--no-debug", default=False)
def main(debug):
    print(debug)


@main.command()
def sub_func1():
    print("running sub_func1")


@main.group()
def sub_func2():
    pass


@sub_func2.command()
def sub_sub_func1():
    print("running sub_sub_func1")


if __name__ == "__main__":
    quick.gui_it(main)
