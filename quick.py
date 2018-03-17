import sys

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

import click

class GListView(QtWidgets.QListView):
    def __init__(self, nargs):
        # TODO: nargs should include type information.
        super(GListView, self).__init__()
        self.nargs = nargs
        self.model = GItemModel(1, parent=self, opt_type=click.STRING)
        self.setModel(self.model)
        self.delegate = GEditDelegate(self)
        self.setItemDelegate(self.delegate)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setToolTip(
                "'a': add a new item blow the selected one\n"
                "'d': delete the selected item"
        )

    def keyPressEvent(self, e):
        if self.nargs == -1:
            if e.key() == QtCore.Qt.Key_A:
                for i in self.selectedIndexes():
                    self.model.insertRow(i.row()+1)
            if e.key() == QtCore.Qt.Key_D:
                si = self.selectedIndexes()
                if self.model.rowCount() > 1:
                    for i in si:
                        self.model.removeRow(i.row())
        super(GListView, self).keyPressEvent(e)


class GItemModel(QtGui.QStandardItemModel):
    def __init__(self, n, parent=None, opt_type=click.STRING, default=None):
        super(QtGui.QStandardItemModel, self).__init__(n, 1, parent)
        self.type = opt_type
        for row in range(n):
            index = self.index(row, 0, QtCore.QModelIndex())
            if default is None or default == "":
                self.setData(index, QtGui.QBrush(QtGui.QColor(100,100,100)),
                        role=QtCore.Qt.ForegroundRole)
            else:
                self.setData(index, default[row])

    def insertRow(self, idx):
        super(GItemModel, self).insertRow(idx)
        index = self.index(idx, 0, QtCore.QModelIndex())
        print(index.row())
        self.setData(index, QtGui.QBrush(QtGui.QColor(100,100,100)),  role=QtCore.Qt.ForegroundRole)


    def data(self, index, role=QtCore.Qt.DisplayRole):

        if role == QtCore.Qt.DisplayRole:
            dstr = QtGui.QStandardItemModel.data(self, index, role)
            if dstr == "" or dstr is None:
                if isinstance(self.type, click.types.Tuple):
                    row = index.row()
                    if 0 <= row < len(self.type.types):
                        tp = self.type.types[row]
                        dstr = tp.name
                else:
                    dstr = self.type.name
                return dstr


        if role == QtCore.Qt.UserRole:
            tp = click.STRING
            if isinstance(self.type, click.types.Tuple):
                row = index.row()
                if 0 <= row < len(self.type.types):
                    tp = self.type.types[row]
            elif isinstance(self.type, click.types.ParamType):
                tp = self.type
            return tp

        return QtGui.QStandardItemModel.data(self, index, role)

class GEditDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        led = QtWidgets.QLineEdit(parent)
        tp = index.data(role=QtCore.Qt.UserRole)
        led.setPlaceholderText(tp.name)
        led.setValidator(select_type_validator(tp))
        return led

    def setEditorData(self, editor, index):
        item_var = index.data(role=QtCore.Qt.EditRole)
        if item_var is not None:
            editor.setText(str(item_var))

    def setModelData(self, editor, model, index):
        data_str = editor.text()
        if data_str == "" or data_str is None:
            model.setData(index, QtGui.QBrush(QtGui.QColor(100,100,100)),  role=QtCore.Qt.ForegroundRole)
        else:
            model.setData(index, QtGui.QBrush(QtGui.QColor('black')),  role=QtCore.Qt.ForegroundRole)
        QtWidgets.QStyledItemDelegate.setModelData(self, editor, model, index)

def generate_label(opt):
    param = QtWidgets.QLabel(opt.name)
    param.setToolTip(opt.help)
    return param


class GStringLineEditor(click.types.StringParamType):
    def to_widget(self, validator=None):
        value = QtWidgets.QLineEdit()
        value.setPlaceholderText(self.type.name)
        if self.default:
            value.setText(str(self.default))
        if self.hide_input:
            value.setEchoMode(QtWidgets.QLineEdit.Password)
        value.setValidator(validator)

        def to_command():
            return [self.opts[0], value.text()]
        return [generate_label(self), value], to_command


class GIntLineEditor(GStringLineEditor):
    def to_widget(self):
        return GStringLineEditor.to_widget(self,
                validator=QtGui.QIntValidator())

class GFloatLineEditor(GStringLineEditor):
    def to_widget(self):
        return GStringLineEditor.to_widget(self,
                validator=QtGui.QDoubleValidator())

class GFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(GFileDialog, self).__init__(*args, **kwargs)
        self.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        self.setLabelText(QtWidgets.QFileDialog.Accept, "Select")
        # self.setFileMode(QFileDialog.Directory)
        # self.setLabelText(QFileDialog.LookIn, "Select")
        # self.setFileMode(QFileDialog.AnyFile)
        # self.setFileMode(QFileDialog.ExistingFiles)

    def accept(self):
        # super(FileDialog, self).accept()
        super(GFileDialog, self).done(QtWidgets.QFileDialog.Accepted)

class GLineEdit_path(QtWidgets.QLineEdit):
    def __init__(self):
        super(GLineEdit_path, self).__init__()
        self.action = self.addAction(
                self.style().standardIcon(QtWidgets.QStyle.SP_DirIcon),
                QtWidgets.QLineEdit.TrailingPosition
                )
        self.fdlg = GFileDialog(self, "Select File Dialog", "./", "*.*")
        self.action.triggered.connect(self.run_dialog)

    def run_dialog(self):
        if self.fdlg.exec() == QtWidgets.QFileDialog.Accepted:
            self.setText(self.fdlg.selectedFiles()[0])

class GPathLindEidt(click.types.Path):
    def to_widget(self):
        value = GLineEdit_path()
        value.setPlaceholderText(self.type.name)
        if self.default:
            value.setText(str(self.default))

        def to_command():
            return [self.opts[0], value.text()]
        return [generate_label(self), value], to_command



class GIntRangeSlider(click.types.IntRange):
    def to_widget(self):
        value = QtWidgets.QLineEdit()
        value = QtWidgets.QSlider(Qt.Horizontal)
        value.setMinimum(self.min)
        value.setMaximum(self.max)
        value.setValue((self.min+self.max)//2)
        value.setTickPosition(QtWidgets.QSlider.TicksBelow)

        def to_command():
            return [self.opts[0], str(value.value())]
        return [generate_label(self), value], to_command

class GIntRangeSlider(click.types.IntRange):
    def to_widget(self, opt):
        value = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        value.setMinimum(self.min)
        value.setMaximum(self.max)
        value.setValue((self.min+self.max)//2)
        value.setTickPosition(QtWidgets.QSlider.TicksBelow)
        # value.setTickInterval(5)

        def to_command():
            return [opt.opts[0], str(value.value())]
        return [generate_label(opt), value], to_command

class GIntRangeLineEditor(click.types.IntRange):
    def to_widget(self, opt):
        value = QtWidgets.QLineEdit()
        # TODO: set validator

        def to_command():
            return [opt.opts[0], value.text()]
        return [generate_label(opt), value], to_command

def bool_flag_option(opt):
    checkbox = QtWidgets.QCheckBox(opt.name)
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
    def to_widget(opt):
        cb = QtWidgets.QComboBox()
        cb.addItems(opt.type.choices)

        def to_command():
            return [opt.opts[0], cb.currentText()]
        return [generate_label(opt), cb], to_command

def count_option(opt):
    sb = QtWidgets.QSpinBox()

    def to_command():
        return [opt.opts[0]] * int(sb.text())
    return [generate_label(opt), sb], to_command

class GTupleGListView(click.Tuple):
    def to_widget(self):
        model = GItemModel(self.nargs, opt_type=self.type, default=self.default)
        view = QtWidgets.QListView()
        view.setModel(model)
        delegate = GEditDelegate(view)
        view.setItemDelegate(delegate)

        def to_command():
            _ = [self.opts[0]]
            for idx in range(model.rowCount()):
                _.append(model.item(idx).text())
            return _
        return [generate_label(self), view], to_command


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
    return [QtWidgets.QLabel(opt.name), value], to_command

def select_type_validator(tp: click.types.ParamType)-> QtGui.QValidator:
    """ select the right validator for `tp`"""
    if isinstance(tp, click.types.IntParamType):
        return QtGui.QIntValidator()
    elif isinstance(tp, click.types.FloatParamType):
        return QtGui.QDoubleValidator()
    return None


def select_opt_validator(opt):
    """ select the right validator for `opt`"""
    return select_type_validator(opt.type) 

def text_arguement(opt):
    param = QtWidgets.QLabel(opt.name)
    value = QtWidgets.QLineEdit()
    if opt.default:
        value.setText(str(opt.default))
    # add validator
    value.setValidator(select_opt_validator(opt))

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
        if opt.nargs > 1 :
            return GTupleGListView.to_widget(opt)
        elif opt.nargs == -1:
            return multi_text_option(opt)
        elif opt.is_bool_flag:
            return bool_flag_option(opt)
        elif opt.count:
            return count_option(opt)
        elif isinstance(opt.type, click.types.Choice):
            return GChoiceComboBox.to_widget(opt)
        elif isinstance(opt.type, click.types.Path):
            return GPathLindEidt.to_widget(opt)
        elif isinstance(opt.type, click.types.IntRange):
            return GIntRangeSlider(opt.type.min, opt.type.max).to_widget(opt)
        elif isinstance(opt.type, click.types.IntParamType):
            return GIntLineEditor.to_widget(opt)
        elif isinstance(opt.type, click.types.FloatParamType):
            return GFloatLineEditor.to_widget(opt)
        else:
            return GStringLineEditor.to_widget(opt)


def layout_append_opts(layout, opts):
    params_func = []
    i = 0
    for i, para in enumerate(opts):
        widget, value_func = opt_to_widget(para)
        params_func.append(value_func)
        for idx, w in enumerate(widget):
            if isinstance(w, QtWidgets.QLayout):
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
        self.grid = QtWidgets.QGridLayout()
        self.grid.setSpacing(10)
        self.grid, self.params_func =\
            layout_append_opts(self.grid, self.func.params)

    def add_sysargv(self):
        sys.argv += generate_sysargv(
            [(self.func.name, self.params_func)]
        )
        # self.func(standalone_mode=self.run_exit)


class App(QtWidgets.QWidget):
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
            button = QtWidgets.QPushButton('run')
            self.group_opt_set.grid.addWidget(
                button, self.group_opt_set.grid.rowCount()+1, 0
            )
            # connect button to function on_click
            button.clicked.connect(self.clean_sysargv)
            button.clicked.connect(self.group_opt_set.add_sysargv)
            button.clicked.connect(self.run_cmd)
        else:
            self.tabs = QtWidgets.QTabWidget()
            self.tab_widget_list = []
            self.cmd_opt_list= []
            for cmd, f in self.func.commands.items():
                tab = QtWidgets.QWidget()
                opt_set = OptionWidgetSet(f, run_exit)
                self.cmd_opt_list.append(opt_set)
                tab.layout = self.cmd_opt_list[-1].grid
                # Add tabs
                self.tabs.addTab(tab, cmd)
                tab.setLayout(tab.layout)
                self.tab_widget_list.append(tab)

                button = QtWidgets.QPushButton('run')
                opt_set.grid.addWidget(button, opt_set.grid.rowCount()+1, 0)

                # connect button to function on_click
                button.clicked.connect(self.clean_sysargv)
                button.clicked.connect(self.group_opt_set.add_sysargv)
                button.clicked.connect(opt_set.add_sysargv)
                button.clicked.connect(self.run_cmd)

            self.group_opt_set.grid.addWidget(self.tabs)

        self.setLayout(self.group_opt_set.grid)

        self.show()

    @QtCore.pyqtSlot()
    def clean_sysargv(self):
        sys.argv = []

    @QtCore.pyqtSlot()
    def run_cmd(self):
        print(sys.argv)
        try:
            self.func(standalone_mode=self.run_exit)
        except click.exceptions.BadParameter as bpe:
            # warning message
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(bpe.format_message())
            msg.exec_()


def gui_it(click_func, run_exit:bool=False)->None:
    app = QtWidgets.QApplication(sys.argv)
    ex = App(click_func, run_exit)
    sys.exit(app.exec_())


def gui_option(f:click.core.BaseCommand)->click.core.BaseCommand:
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
