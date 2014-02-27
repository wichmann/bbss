# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bbss_tabbed_gui.ui'
#
# Created: Thu Feb 27 11:27:26 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_BBSS_Main_Window(object):
    def setupUi(self, BBSS_Main_Window):
        BBSS_Main_Window.setObjectName(_fromUtf8("BBSS_Main_Window"))
        BBSS_Main_Window.resize(660, 505)
        self.centralwidget = QtGui.QWidget(BBSS_Main_Window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.TaskTabbedPane = QtGui.QTabWidget(self.centralwidget)
        self.TaskTabbedPane.setGeometry(QtCore.QRect(10, 0, 641, 461))
        self.TaskTabbedPane.setMinimumSize(QtCore.QSize(641, 451))
        self.TaskTabbedPane.setObjectName(_fromUtf8("TaskTabbedPane"))
        self.import_tab = QtGui.QWidget()
        self.import_tab.setObjectName(_fromUtf8("import_tab"))
        self.gridLayoutWidget = QtGui.QWidget(self.import_tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 611, 411))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.import_data_button = QtGui.QPushButton(self.gridLayoutWidget)
        self.import_data_button.setObjectName(_fromUtf8("import_data_button"))
        self.gridLayout.addWidget(self.import_data_button, 3, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.load_file_button = QtGui.QPushButton(self.gridLayoutWidget)
        self.load_file_button.setObjectName(_fromUtf8("load_file_button"))
        self.gridLayout.addWidget(self.load_file_button, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.delete_database_button = QtGui.QPushButton(self.gridLayoutWidget)
        self.delete_database_button.setObjectName(_fromUtf8("delete_database_button"))
        self.gridLayout.addWidget(self.delete_database_button, 3, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.import_data_tableview = QtGui.QTableView(self.gridLayoutWidget)
        self.import_data_tableview.setObjectName(_fromUtf8("import_data_tableview"))
        self.gridLayout.addWidget(self.import_data_tableview, 1, 0, 1, 3)
        self.import_filter_text = QtGui.QLineEdit(self.gridLayoutWidget)
        self.import_filter_text.setObjectName(_fromUtf8("import_filter_text"))
        self.gridLayout.addWidget(self.import_filter_text, 2, 0, 1, 3)
        self.TaskTabbedPane.addTab(self.import_tab, _fromUtf8(""))
        self.export_tab = QtGui.QWidget()
        self.export_tab.setObjectName(_fromUtf8("export_tab"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.export_tab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 611, 411))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.export_ad_button = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.export_ad_button.setObjectName(_fromUtf8("export_ad_button"))
        self.gridLayout_2.addWidget(self.export_ad_button, 2, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.search_button = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.search_button.setObjectName(_fromUtf8("search_button"))
        self.gridLayout_2.addWidget(self.search_button, 2, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.export_data_button = QtGui.QPushButton(self.gridLayoutWidget_2)
        self.export_data_button.setObjectName(_fromUtf8("export_data_button"))
        self.gridLayout_2.addWidget(self.export_data_button, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.export_data_tableview = QtGui.QTableView(self.gridLayoutWidget_2)
        self.export_data_tableview.setObjectName(_fromUtf8("export_data_tableview"))
        self.gridLayout_2.addWidget(self.export_data_tableview, 0, 0, 1, 3)
        self.export_filter_text = QtGui.QLineEdit(self.gridLayoutWidget_2)
        self.export_filter_text.setObjectName(_fromUtf8("export_filter_text"))
        self.gridLayout_2.addWidget(self.export_filter_text, 1, 0, 1, 3)
        self.TaskTabbedPane.addTab(self.export_tab, _fromUtf8(""))
        self.options_tab = QtGui.QWidget()
        self.options_tab.setObjectName(_fromUtf8("options_tab"))
        self.verticalLayoutWidget = QtGui.QWidget(self.options_tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 611, 201))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(-1)
        self.verticalLayout.setContentsMargins(25, -1, 25, -1)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.replace_classnames_checkbox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.replace_classnames_checkbox.setObjectName(_fromUtf8("replace_classnames_checkbox"))
        self.verticalLayout.addWidget(self.replace_classnames_checkbox)
        self.replace_characters_checkbox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.replace_characters_checkbox.setObjectName(_fromUtf8("replace_characters_checkbox"))
        self.verticalLayout.addWidget(self.replace_characters_checkbox)
        self.store_in_db_checkbox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.store_in_db_checkbox.setObjectName(_fromUtf8("store_in_db_checkbox"))
        self.verticalLayout.addWidget(self.store_in_db_checkbox)
        self.bonus_function_checkbox = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.bonus_function_checkbox.setObjectName(_fromUtf8("bonus_function_checkbox"))
        self.verticalLayout.addWidget(self.bonus_function_checkbox)
        self.TaskTabbedPane.addTab(self.options_tab, _fromUtf8(""))
        BBSS_Main_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(BBSS_Main_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 660, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuDatei = QtGui.QMenu(self.menubar)
        self.menuDatei.setObjectName(_fromUtf8("menuDatei"))
        BBSS_Main_Window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(BBSS_Main_Window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        BBSS_Main_Window.setStatusBar(self.statusbar)
        self.menu_exit = QtGui.QAction(BBSS_Main_Window)
        self.menu_exit.setObjectName(_fromUtf8("menu_exit"))
        self.menuDatei.addAction(self.menu_exit)
        self.menubar.addAction(self.menuDatei.menuAction())

        self.retranslateUi(BBSS_Main_Window)
        self.TaskTabbedPane.setCurrentIndex(0)
        QtCore.QObject.connect(self.menu_exit, QtCore.SIGNAL(_fromUtf8("activated()")), BBSS_Main_Window.close)
        QtCore.QMetaObject.connectSlotsByName(BBSS_Main_Window)

    def retranslateUi(self, BBSS_Main_Window):
        BBSS_Main_Window.setWindowTitle(_translate("BBSS_Main_Window", "BBSS", None))
        self.import_data_button.setText(_translate("BBSS_Main_Window", "Daten importieren...", None))
        self.load_file_button.setText(_translate("BBSS_Main_Window", "Datei laden...", None))
        self.delete_database_button.setText(_translate("BBSS_Main_Window", "Delete Database...", None))
        self.TaskTabbedPane.setTabText(self.TaskTabbedPane.indexOf(self.import_tab), _translate("BBSS_Main_Window", "Daten importieren", None))
        self.export_ad_button.setText(_translate("BBSS_Main_Window", "Daten in AD schreiben...", None))
        self.search_button.setText(_translate("BBSS_Main_Window", "Suchen...", None))
        self.export_data_button.setText(_translate("BBSS_Main_Window", "Daten exportieren...", None))
        self.TaskTabbedPane.setTabText(self.TaskTabbedPane.indexOf(self.export_tab), _translate("BBSS_Main_Window", "Daten exportieren", None))
        self.replace_classnames_checkbox.setText(_translate("BBSS_Main_Window", "Klassennamen ersetzen", None))
        self.replace_characters_checkbox.setText(_translate("BBSS_Main_Window", "Illegale Zeichen in Namen ersetzen", None))
        self.store_in_db_checkbox.setText(_translate("BBSS_Main_Window", "Daten in Datenbank ablegen", None))
        self.bonus_function_checkbox.setText(_translate("BBSS_Main_Window", "Super-Duper-Funktion aktivieren", None))
        self.TaskTabbedPane.setTabText(self.TaskTabbedPane.indexOf(self.options_tab), _translate("BBSS_Main_Window", "Optionen", None))
        self.menuDatei.setTitle(_translate("BBSS_Main_Window", "Datei", None))
        self.menu_exit.setText(_translate("BBSS_Main_Window", "Beenden", None))

