# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bbss_tabbed_gui.ui'
#
# Created: Tue Sep 22 07:21:47 2015
#      by: PyQt4 UI code generator 4.11.3
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
        BBSS_Main_Window.resize(657, 789)
        self.centralwidget = QtGui.QWidget(BBSS_Main_Window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.TaskTabbedPane = QtGui.QTabWidget(self.centralwidget)
        self.TaskTabbedPane.setGeometry(QtCore.QRect(10, 10, 641, 731))
        self.TaskTabbedPane.setMinimumSize(QtCore.QSize(641, 451))
        self.TaskTabbedPane.setObjectName(_fromUtf8("TaskTabbedPane"))
        self.import_tab = QtGui.QWidget()
        self.import_tab.setObjectName(_fromUtf8("import_tab"))
        self.gridLayoutWidget = QtGui.QWidget(self.import_tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 611, 681))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.load_file_button = QtGui.QPushButton(self.gridLayoutWidget)
        self.load_file_button.setObjectName(_fromUtf8("load_file_button"))
        self.gridLayout.addWidget(self.load_file_button, 5, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_8 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 3)
        self.import_data_button = QtGui.QPushButton(self.gridLayoutWidget)
        self.import_data_button.setObjectName(_fromUtf8("import_data_button"))
        self.gridLayout.addWidget(self.import_data_button, 5, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.import_data_tableview = QtGui.QTableView(self.gridLayoutWidget)
        self.import_data_tableview.setObjectName(_fromUtf8("import_data_tableview"))
        self.gridLayout.addWidget(self.import_data_tableview, 1, 0, 1, 3)
        self.delete_database_button = QtGui.QPushButton(self.gridLayoutWidget)
        self.delete_database_button.setObjectName(_fromUtf8("delete_database_button"))
        self.gridLayout.addWidget(self.delete_database_button, 5, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(10, 5, 10, 5)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(52, 0))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.import_filter_text = QtGui.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.import_filter_text.sizePolicy().hasHeightForWidth())
        self.import_filter_text.setSizePolicy(sizePolicy)
        self.import_filter_text.setMaxLength(50)
        self.import_filter_text.setObjectName(_fromUtf8("import_filter_text"))
        self.horizontalLayout_2.addWidget(self.import_filter_text)
        self.search_result_label = QtGui.QLabel(self.gridLayoutWidget)
        self.search_result_label.setMinimumSize(QtCore.QSize(200, 0))
        self.search_result_label.setText(_fromUtf8(""))
        self.search_result_label.setObjectName(_fromUtf8("search_result_label"))
        self.horizontalLayout_2.addWidget(self.search_result_label)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 3)
        self.TaskTabbedPane.addTab(self.import_tab, _fromUtf8(""))
        self.export_tab = QtGui.QWidget()
        self.export_tab.setObjectName(_fromUtf8("export_tab"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.export_tab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 611, 683))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gridLayoutWidget_2)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.added_student_table_label = QtGui.QLabel(self.gridLayoutWidget_2)
        self.added_student_table_label.setObjectName(_fromUtf8("added_student_table_label"))
        self.verticalLayout.addWidget(self.added_student_table_label)
        self.added_students_tableview = QtGui.QTableView(self.gridLayoutWidget_2)
        self.added_students_tableview.setMinimumSize(QtCore.QSize(0, 150))
        self.added_students_tableview.setObjectName(_fromUtf8("added_students_tableview"))
        self.added_students_tableview.verticalHeader().setMinimumSectionSize(4)
        self.verticalLayout.addWidget(self.added_students_tableview)
        self.removed_student_table_label = QtGui.QLabel(self.gridLayoutWidget_2)
        self.removed_student_table_label.setObjectName(_fromUtf8("removed_student_table_label"))
        self.verticalLayout.addWidget(self.removed_student_table_label)
        self.removed_students_tableview = QtGui.QTableView(self.gridLayoutWidget_2)
        self.removed_students_tableview.setMinimumSize(QtCore.QSize(0, 150))
        self.removed_students_tableview.setObjectName(_fromUtf8("removed_students_tableview"))
        self.verticalLayout.addWidget(self.removed_students_tableview)
        self.export_group = QtGui.QGroupBox(self.gridLayoutWidget_2)
        self.export_group.setMinimumSize(QtCore.QSize(0, 150))
        self.export_group.setObjectName(_fromUtf8("export_group"))
        self.export_data_button = QtGui.QPushButton(self.export_group)
        self.export_data_button.setGeometry(QtCore.QRect(450, 90, 131, 31))
        self.export_data_button.setObjectName(_fromUtf8("export_data_button"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.export_group)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(310, 40, 273, 33))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.old_import_number = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.old_import_number.setMaxLength(3)
        self.old_import_number.setObjectName(_fromUtf8("old_import_number"))
        self.horizontalLayout.addWidget(self.old_import_number, QtCore.Qt.AlignHCenter)
        self.label_4 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.new_import_number = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.new_import_number.setMaxLength(3)
        self.new_import_number.setObjectName(_fromUtf8("new_import_number"))
        self.horizontalLayout.addWidget(self.new_import_number, QtCore.Qt.AlignHCenter)
        self.export_format_combobox = QtGui.QComboBox(self.export_group)
        self.export_format_combobox.setGeometry(QtCore.QRect(120, 40, 161, 31))
        self.export_format_combobox.setObjectName(_fromUtf8("export_format_combobox"))
        self.label_5 = QtGui.QLabel(self.export_group)
        self.label_5.setGeometry(QtCore.QRect(20, 50, 91, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.export_group)
        self.TaskTabbedPane.addTab(self.export_tab, _fromUtf8(""))
        self.search_tab = QtGui.QWidget()
        self.search_tab.setObjectName(_fromUtf8("search_tab"))
        self.verticalLayoutWidget = QtGui.QWidget(self.search_tab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 611, 351))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.search_students_label = QtGui.QLabel(self.verticalLayoutWidget)
        self.search_students_label.setObjectName(_fromUtf8("search_students_label"))
        self.verticalLayout_3.addWidget(self.search_students_label)
        self.search_students_tableView = QtGui.QTableView(self.verticalLayoutWidget)
        self.search_students_tableView.setObjectName(_fromUtf8("search_students_tableView"))
        self.verticalLayout_3.addWidget(self.search_students_tableView)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(10, 5, 10, 5)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_6 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.search_student_text = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.search_student_text.setObjectName(_fromUtf8("search_student_text"))
        self.horizontalLayout_3.addWidget(self.search_student_text)
        self.clear_search_field_button = QtGui.QToolButton(self.verticalLayoutWidget)
        self.clear_search_field_button.setObjectName(_fromUtf8("clear_search_field_button"))
        self.horizontalLayout_3.addWidget(self.clear_search_field_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.groupBox = QtGui.QGroupBox(self.search_tab)
        self.groupBox.setGeometry(QtCore.QRect(10, 370, 611, 311))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayoutWidget_3 = QtGui.QWidget(self.groupBox)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(20, 30, 571, 263))
        self.gridLayoutWidget_3.setObjectName(_fromUtf8("gridLayoutWidget_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_2.setMargin(5)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 4, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)
        self.label_12 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 5, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.gridLayoutWidget_3)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_2.addWidget(self.label_13, 6, 0, 1, 1)
        self.result_surname_text = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.result_surname_text.setReadOnly(True)
        self.result_surname_text.setObjectName(_fromUtf8("result_surname_text"))
        self.gridLayout_2.addWidget(self.result_surname_text, 0, 1, 1, 1)
        self.result_name_text = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.result_name_text.setReadOnly(True)
        self.result_name_text.setObjectName(_fromUtf8("result_name_text"))
        self.gridLayout_2.addWidget(self.result_name_text, 1, 1, 1, 1)
        self.result_class_text = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.result_class_text.setReadOnly(True)
        self.result_class_text.setObjectName(_fromUtf8("result_class_text"))
        self.gridLayout_2.addWidget(self.result_class_text, 2, 1, 1, 1)
        self.result_birthday_text = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.result_birthday_text.setReadOnly(True)
        self.result_birthday_text.setObjectName(_fromUtf8("result_birthday_text"))
        self.gridLayout_2.addWidget(self.result_birthday_text, 3, 1, 1, 1)
        self.result_username_text = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.result_username_text.setReadOnly(True)
        self.result_username_text.setObjectName(_fromUtf8("result_username_text"))
        self.gridLayout_2.addWidget(self.result_username_text, 4, 1, 1, 1)
        self.result_password_text = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.result_password_text.setReadOnly(True)
        self.result_password_text.setObjectName(_fromUtf8("result_password_text"))
        self.gridLayout_2.addWidget(self.result_password_text, 5, 1, 1, 1)
        self.result_imports_text = QtGui.QLineEdit(self.gridLayoutWidget_3)
        self.result_imports_text.setReadOnly(True)
        self.result_imports_text.setObjectName(_fromUtf8("result_imports_text"))
        self.gridLayout_2.addWidget(self.result_imports_text, 6, 1, 1, 1)
        self.TaskTabbedPane.addTab(self.search_tab, _fromUtf8(""))
        self.options_tab = QtGui.QWidget()
        self.options_tab.setObjectName(_fromUtf8("options_tab"))
        self.options_group = QtGui.QGroupBox(self.options_tab)
        self.options_group.setGeometry(QtCore.QRect(10, 10, 611, 221))
        self.options_group.setObjectName(_fromUtf8("options_group"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.options_group)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 30, 571, 121))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.replace_classnames_checkbox = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.replace_classnames_checkbox.setChecked(True)
        self.replace_classnames_checkbox.setObjectName(_fromUtf8("replace_classnames_checkbox"))
        self.verticalLayout_2.addWidget(self.replace_classnames_checkbox)
        self.replace_characters_checkbox = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.replace_characters_checkbox.setChecked(True)
        self.replace_characters_checkbox.setObjectName(_fromUtf8("replace_characters_checkbox"))
        self.verticalLayout_2.addWidget(self.replace_characters_checkbox)
        self.store_in_db_checkbox = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.store_in_db_checkbox.setChecked(True)
        self.store_in_db_checkbox.setObjectName(_fromUtf8("store_in_db_checkbox"))
        self.verticalLayout_2.addWidget(self.store_in_db_checkbox)
        self.settings_group = QtGui.QGroupBox(self.options_tab)
        self.settings_group.setGeometry(QtCore.QRect(10, 250, 611, 431))
        self.settings_group.setObjectName(_fromUtf8("settings_group"))
        self.verticalLayoutWidget_3 = QtGui.QWidget(self.settings_group)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20, 30, 571, 391))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_8.setMargin(0)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.label_18 = QtGui.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_18.setFont(font)
        self.label_18.setTextFormat(QtCore.Qt.AutoText)
        self.label_18.setScaledContents(False)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.verticalLayout_8.addWidget(self.label_18)
        self.label_19 = QtGui.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_19.setFont(font)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setWordWrap(True)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.verticalLayout_8.addWidget(self.label_19)
        self.line_2 = QtGui.QFrame(self.verticalLayoutWidget_3)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout_8.addWidget(self.line_2)
        self.label_20 = QtGui.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_20.setFont(font)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.verticalLayout_8.addWidget(self.label_20)
        self.label_21 = QtGui.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_21.setFont(font)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.verticalLayout_8.addWidget(self.label_21)
        self.TaskTabbedPane.addTab(self.options_tab, _fromUtf8(""))
        BBSS_Main_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(BBSS_Main_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 657, 29))
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
        self.label_8.setBuddy(self.import_data_tableview)
        self.label.setBuddy(self.import_filter_text)
        self.added_student_table_label.setBuddy(self.added_students_tableview)
        self.removed_student_table_label.setBuddy(self.removed_students_tableview)
        self.label_3.setBuddy(self.old_import_number)
        self.label_4.setBuddy(self.new_import_number)
        self.label_5.setBuddy(self.export_format_combobox)

        self.retranslateUi(BBSS_Main_Window)
        self.TaskTabbedPane.setCurrentIndex(2)
        QtCore.QObject.connect(self.menu_exit, QtCore.SIGNAL(_fromUtf8("activated()")), BBSS_Main_Window.close)
        QtCore.QMetaObject.connectSlotsByName(BBSS_Main_Window)

    def retranslateUi(self, BBSS_Main_Window):
        BBSS_Main_Window.setWindowTitle(_translate("BBSS_Main_Window", "BBSS", None))
        self.load_file_button.setText(_translate("BBSS_Main_Window", "Datei laden...", None))
        self.label_8.setText(_translate("BBSS_Main_Window", "Importierte Schüler:", None))
        self.import_data_button.setText(_translate("BBSS_Main_Window", "Daten importieren...", None))
        self.delete_database_button.setText(_translate("BBSS_Main_Window", "Lösche Datenbank...", None))
        self.label.setText(_translate("BBSS_Main_Window", "Suche:", None))
        self.TaskTabbedPane.setTabText(self.TaskTabbedPane.indexOf(self.import_tab), _translate("BBSS_Main_Window", "Daten importieren", None))
        self.added_student_table_label.setText(_translate("BBSS_Main_Window", "Hinzugefügte Schüler:", None))
        self.removed_student_table_label.setText(_translate("BBSS_Main_Window", "Gelöschte Schüler:", None))
        self.export_group.setTitle(_translate("BBSS_Main_Window", "Exportieren...", None))
        self.export_data_button.setText(_translate("BBSS_Main_Window", "Daten exportieren...", None))
        self.label_3.setText(_translate("BBSS_Main_Window", "von", None))
        self.old_import_number.setText(_translate("BBSS_Main_Window", "0", None))
        self.label_4.setText(_translate("BBSS_Main_Window", "bis", None))
        self.new_import_number.setText(_translate("BBSS_Main_Window", "0", None))
        self.label_5.setText(_translate("BBSS_Main_Window", "Exportformat:", None))
        self.TaskTabbedPane.setTabText(self.TaskTabbedPane.indexOf(self.export_tab), _translate("BBSS_Main_Window", "Daten exportieren", None))
        self.search_students_label.setText(_translate("BBSS_Main_Window", "Schüler suchen:", None))
        self.label_6.setText(_translate("BBSS_Main_Window", "Suche: ", None))
        self.clear_search_field_button.setText(_translate("BBSS_Main_Window", "X", None))
        self.groupBox.setTitle(_translate("BBSS_Main_Window", "Schülerinformationen", None))
        self.label_2.setText(_translate("BBSS_Main_Window", "Vorname", None))
        self.label_7.setText(_translate("BBSS_Main_Window", "Name", None))
        self.label_11.setText(_translate("BBSS_Main_Window", "Benutzername", None))
        self.label_9.setText(_translate("BBSS_Main_Window", "Klasse", None))
        self.label_10.setText(_translate("BBSS_Main_Window", "Geburtsdatum", None))
        self.label_12.setText(_translate("BBSS_Main_Window", "Passwort", None))
        self.label_13.setText(_translate("BBSS_Main_Window", "Importe", None))
        self.TaskTabbedPane.setTabText(self.TaskTabbedPane.indexOf(self.search_tab), _translate("BBSS_Main_Window", "Schüler suchen", None))
        self.options_group.setTitle(_translate("BBSS_Main_Window", "Optionen", None))
        self.replace_classnames_checkbox.setText(_translate("BBSS_Main_Window", "Klassennamen ersetzen", None))
        self.replace_characters_checkbox.setText(_translate("BBSS_Main_Window", "Illegale Zeichen in Namen ersetzen", None))
        self.store_in_db_checkbox.setText(_translate("BBSS_Main_Window", "Daten in Datenbank ablegen", None))
        self.settings_group.setTitle(_translate("BBSS_Main_Window", "Über...", None))
        self.label_18.setText(_translate("BBSS_Main_Window", "bbss - BBS Student Management", None))
        self.label_19.setText(_translate("BBSS_Main_Window", "Software für das Erzeugen und Verwalten von Schülern und ihrer Benutzernamen und Passwörtern.", None))
        self.label_20.setText(_translate("BBSS_Main_Window", "Autor: Christian Wichmann", None))
        self.label_21.setText(_translate("BBSS_Main_Window", "Lizensiert unter der GNU GPL v2 oder neuer.", None))
        self.TaskTabbedPane.setTabText(self.TaskTabbedPane.indexOf(self.options_tab), _translate("BBSS_Main_Window", "Optionen", None))
        self.menuDatei.setTitle(_translate("BBSS_Main_Window", "Datei", None))
        self.menu_exit.setText(_translate("BBSS_Main_Window", "Beenden", None))

