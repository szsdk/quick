import quick
import click
import unittest

import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtTest import QTest

@click.command()
@click.option("--name", type=click.types.Choice(["peng", "bo"]))
def select_name(name):
    pass

class TestFunction(unittest.TestCase):
    def setUp(self):
        self._app = QtWidgets.QApplication(sys.argv)
        
    def test_opt_to_widget(self):
        self.assertIsInstance(quick.opt_to_widget(select_name.params[0])[0][1], QtWidgets.QComboBox)

if __name__ == "__main__":
    unittest.main()
