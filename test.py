from guick import gui_it
import click

@click.command()
@click.option("--hello", help="say hello")
@click.option("--add", type=int, help="input an integer number")
@click.option("--times", type=float, help="input a double number")
def example_cmd(hello, add, times):
    print("hello:", hello, type(hello))
    print("add:", add, type(add))
    print("times:", times, type(times))


if __name__ == "__main__":
    gui_it(example_cmd)
