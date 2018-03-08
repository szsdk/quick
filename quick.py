import sys
# from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
### For high dpi screen
# from PyQt5 import QtCore
# if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    # QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

# if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    # QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

import click

class GListView(QListView):
    def __init__(self, nargs):
        # TODO: nargs should include type information.
        super().__init__()
        self.nargs = nargs
        self.model = QStandardItemModel(self)
        if nargs > 0:
            for _ in range(nargs):
                item = QStandardItem()
                self.model.appendRow(item)
        else:
            self.model.appendRow(QStandardItem())
        self.setModel(self.model)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def keyPressEvent(self, e):
        if self.nargs == -1:
            if e.key() == Qt.Key_Delete:
                for i in self.selectedIndexes():
                    self.model.removeRow(i.row())
            elif e.key() == Qt.Key_T:
                for i in self.selectedIndexes():
                    self.model.insertRow(i.row())
        super(GListView, self).keyPressEvent(e)


def generate_label(opt):
    param = QLabel(opt.name)
    param.setToolTip(opt.help)
    return param

class GStringLineEditor(click.types.StringParamType):
    @staticmethod
    def to_widget(opt):
        value = QLineEdit()
        if opt.default:
            value.setText(str(opt.default))
        if opt.hide_input:
            value.setEchoMode(QLineEdit.Password)

        def to_command():
            return [opt.opts[0], value.text()]
        return [generate_label(opt), value], to_command


class GIntLineEditor(GStringLineEditor):
    @staticmethod
    def to_widget(opt):
        [param, value], to_command = GStringLineEditor.to_widget(opt)
        value.setValidator(QIntValidator())
        return [param, value], to_command

class GFloatLineEditor(GStringLineEditor):
    @staticmethod
    def to_widget(opt):
        [param, value], to_command = GStringLineEditor.to_widget(opt)
        value.setValidator(QDoubleValidator())
        return [param, value], to_command

class GIntRangeSlider(click.types.IntRange):
    def to_widget(self, opt):
        value = QLineEdit()
        value = QSlider(Qt.Horizontal)
        value.setMinimum(self.min)
        value.setMaximum(self.max)
        value.setValue((self.min+self.max)//2)
        value.setTickPosition(QSlider.TicksBelow)
        # value.setTickInterval(5)

        def to_command():
            return [opt.opts[0], str(value.value())]
        return [generate_label(opt), value], to_command

class GIntRangeSlider(click.types.IntRange):
    def to_widget(self, opt):
        value = QSlider(Qt.Horizontal)
        value.setMinimum(self.min)
        value.setMaximum(self.max)
        value.setValue((self.min+self.max)//2)
        value.setTickPosition(QSlider.TicksBelow)
        # value.setTickInterval(5)

        def to_command():
            return [opt.opts[0], str(value.value())]
        return [generate_label(opt), value], to_command

class GIntRangeLineEditor(click.types.IntRange):
    def to_widget(self, opt):
        value = QLineEdit()
        # TODO: set validator

        def to_command():
            return [opt.opts[0], value.text()]
        return [generate_label(opt), value], to_command

def bool_flag_option(opt):
    checkbox = QCheckBox(opt.name)
    if opt.default:
        checkbox.setCheckState(2)
    # set tip
    checkbox.setToolTip(opt.help)

    def to_command():
        if checkbox.checkState():
            return [opt.opts[0]]
        else:
            return opt.secondary_opts
    return [checkbox], to_command

class GChoiceComboBox(click.types.Choice):
    @staticmethod
    def to_widget(opt):
        cb = QComboBox()
        cb.addItems(opt.type.choices)

        def to_command():
            return [opt.opts[0], cb.currentText()]
        return [generate_label(opt), cb], to_command

def count_option(opt):
    sb = QSpinBox()

    def to_command():
        return [opt.opts[0]] * int(sb.text())
    return [generate_label(opt), sb], to_command


def multi_text_option(opt):
    value = GListView(opt.nargs)
    def to_command():
        _ = [opt.opts[0]]
        for idx in range(value.model.rowCount()):
            _.append(value.model.item(idx).text())
        return _
    return [generate_label(opt), value], to_command

def multi_text_arguement(opt):
    value = GListView(opt.nargs)
    def to_command():
        _ = []
        for idx in range(value.model.rowCount()):
            _.append(value.model.item(idx).text())
        return _
    return [QLabel(opt.name), value], to_command

def text_arguement(opt):
    param = QLabel(opt.name)
    value = QLineEdit()
    if opt.default:
        value.setText(str(opt.default))
    # add validator
    if isinstance(opt.type, click.types.IntParamType) and opt.nargs == 1:
        value.setValidator(QIntValidator())
    elif isinstance(opt.type, click.types.FloatParamType) and opt.nargs == 1:
        value.setValidator(QDoubleValidator())

    def to_command():
        return [value.text()]
    return [param, value], to_command


def opt_to_widget(opt):
    #customed widget
    if isinstance(opt.type, click.types.FuncParamType):
        if hasattr(opt.type.func, 'to_widget'):
            return opt.type.func.to_widget(opt)
    elif hasattr(opt.type, 'to_widget'):
            return opt.type.to_widget(opt)

    if type(opt) == click.core.Argument:
        if opt.nargs > 1 or opt.nargs == -1:
            return multi_text_arguement(opt)
        else:
            return text_arguement(opt)
    else:
        if opt.nargs > 1 or opt.nargs == -1:
            return multi_text_option(opt)
        elif opt.is_bool_flag:
            return bool_flag_option(opt)
        elif opt.count:
            return count_option(opt)
        elif isinstance(opt.type, click.types.Choice):
            return GChoiceComboBox.to_widget(opt)
        elif isinstance(opt.type, click.types.IntParamType):
            return GIntLineEditor.to_widget(opt)
        elif isinstance(opt.type, click.types.FloatParamType):
            return GFloatLineEditor.to_widget(opt)
        elif isinstance(opt.type, click.types.IntRange):
            return GIntRangeSlider(opt.type.min, opt.type.max).to_widget(opt)
        else:
            return GStringLineEditor.to_widget(opt)


def layout_append_opts(layout, opts):
    params_func = []
    i = 0
    for i, para in enumerate(opts):
        widget, value_func = opt_to_widget(para)
        params_func.append(value_func)
        for idx, w in enumerate(widget):
            if isinstance(w, QLayout):
                layout.addLayout(w, i, idx)
            else:
                layout.addWidget(w, i, idx)
    return layout, params_func

def generate_sysargv(cmd_list):
    argv_list = []
    for name, func_list in cmd_list:
        argv_list.append(name)
        for value_func in func_list:
            argv_list += value_func()
    return argv_list

class OptionWidgetSet(object):
    def __init__(self, func, run_exit):
        self.func = func
        self.run_exit = run_exit
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid, self.params_func =\
            layout_append_opts(self.grid, self.func.params)

    def add_sysargv(self):
        sys.argv += generate_sysargv(
            [(self.func.name, self.params_func)]
        )
        # self.func(standalone_mode=self.run_exit)


class App(QWidget):
    def __init__(self, func, run_exit):
        super().__init__()
        self.title = func.name
        self.func = func
        self.left = 10
        self.top = 10
        self.width = 400
        self.height = 140
        self.initUI(run_exit)

    def initUI(self, run_exit):
        self.run_exit = run_exit
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.group_opt_set = OptionWidgetSet(self.func, self.run_exit)
        if not isinstance(self.func, click.core.Group):
            button = QPushButton('run')
            self.group_opt_set.grid.addWidget(
                button, self.group_opt_set.grid.rowCount()+1, 0
            )
            # connect button to function on_click
            button.clicked.connect(self.clean_sysargv)
            button.clicked.connect(self.group_opt_set.add_sysargv)
            button.clicked.connect(self.run_cmd)
        else:
            self.tabs = QTabWidget()
            self.tab_widget_list = []
            self.cmd_opt_list= []
            for cmd, f in self.func.commands.items():
                tab = QWidget()
                opt_set = OptionWidgetSet(f, run_exit)
                self.cmd_opt_list.append(opt_set)
                tab.layout = self.cmd_opt_list[-1].grid
                # Add tabs
                self.tabs.addTab(tab, cmd)
                tab.setLayout(tab.layout)
                self.tab_widget_list.append(tab)

                button = QPushButton('run')
                opt_set.grid.addWidget(button, opt_set.grid.rowCount()+1, 0)

                # connect button to function on_click
                button.clicked.connect(self.clean_sysargv)
                button.clicked.connect(self.group_opt_set.add_sysargv)
                button.clicked.connect(opt_set.add_sysargv)
                button.clicked.connect(self.run_cmd)

            self.group_opt_set.grid.addWidget(self.tabs)

        self.setLayout(self.group_opt_set.grid)

        self.show()

    @pyqtSlot()
    def clean_sysargv(self):
        sys.argv = []

    @pyqtSlot()
    def run_cmd(self):
        print(sys.argv)
        try:
            self.func(standalone_mode=self.run_exit)
        except click.exceptions.BadParameter as bpe:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(bpe.format_message())
            msg.exec_()


def gui_it(click_func, run_exit=False):
    app = QApplication(sys.argv)
    ex = App(click_func, run_exit)
    # if exit:
    sys.exit(app.exec_())


def gui_option(f):
    """decorator for adding '--gui' option to command"""
    def run_gui_it(ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        f.params = [p for p in f.params if not p.name == "gui"]
        gui_it(f)
        ctx.exit()
    return click.option('--gui', is_flag=True, callback=run_gui_it,
                        help="run with gui",
                        expose_value=False, is_eager=False)(f)
