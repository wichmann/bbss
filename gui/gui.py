
"""
bbss - BBS Student Management

Default graphical user interface for bbss.

Main window was generated by calling:
    pyuic4 bbss_tabbed_gui.ui > main.py

Created on Mon Feb  23 15:08:56 2014

@author: Christian Wichmann
"""

import logging
from PyQt4 import QtGui
from PyQt4 import QtCore

from gui.main import Ui_BBSS_Main_Window
from bbss import bbss


__all__ = ['start_gui']


logger = logging.getLogger('bbss.gui')


APP_NAME = "BBSS"


class StudentTableFilterProxyModel(QtGui.QSortFilterProxyModel):
    """Filters student table for regular expression in all columns."""
    def filterAcceptsRow(self, sourceRow, sourceParent):
        index0 = self.sourceModel().index(sourceRow, 0, sourceParent)
        index1 = self.sourceModel().index(sourceRow, 1, sourceParent)
        index2 = self.sourceModel().index(sourceRow, 2, sourceParent)
        return (self.filterRegExp().indexIn(self.sourceModel().data(index0)) >= 0
                or self.filterRegExp().indexIn(self.sourceModel().data(index1)) >= 0
                or self.filterRegExp().indexIn(self.sourceModel().data(index2)) >= 0)


class StudentTableModel(QtCore.QAbstractTableModel):
    def __init__(self, student_list, parent=None):
        super(StudentTableModel, self).__init__()
        self.student_list = student_list
        self.column_list = ('surname', 'firstname', 'classname', 'birthday')
        self.column_list_i18n = ('Nachname', 'Vorname', 'Klasse', 'Geburtstag')

    def update(self, student_list):
        self.student_list = student_list

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.student_list)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.column_list)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return ''
        elif role != QtCore.Qt.DisplayRole:
            return None
        student = self.student_list[index.row()]
        return '{0}'.format(getattr(student,
                                    self.column_list[index.column()]))

    def headerData(self, count, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.column_list_i18n[count]
            elif orientation == QtCore.Qt.Vertical:
                return str(count+1)

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        logger.warn('Updating of student data not yet implemented.')
        #print "setData", index.row(), index.column(), value

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled
        #if (index.column() == 0):
        #    return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        #else:
        #    return QtCore.Qt.ItemIsEnabled


class BbssGui(QtGui.QMainWindow, Ui_BBSS_Main_Window):
    """Main window for bbss"""

    FILENAME = 'schueler_20140213.csv'

    def __init__(self, parent=None):
        """Initialize main window for bbss."""
        logger.info('Building main window of bbss...')
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #self.resize(QtCore.QSize(1000, 800))
        self.setup_table_models()
        self.setup_combo_boxes()
        self.center_on_screen()
        self.set_signals_and_slots()

    def setup_table_models(self):
        """Sets up table view and its models."""
        # set up import table view
        self.import_table_model = StudentTableModel(bbss.student_list)
        self.proxy_import_table_model = StudentTableFilterProxyModel()
        self.proxy_import_table_model.setSourceModel(self.import_table_model)
        self.proxy_import_table_model.setDynamicSortFilter(True)
        self.import_data_tableview.setModel(self.proxy_import_table_model)
        self.import_data_tableview.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch)
        # set up export table views
        self.added_students_table_model = StudentTableModel(list())
        self.removed_students_table_model = StudentTableModel(list())
        self.added_students_tableview.setModel(
            self.added_students_table_model)
        self.removed_students_tableview.setModel(
            self.removed_students_table_model)
        self.added_students_tableview.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch)
        self.removed_students_tableview.horizontalHeader().setResizeMode(
            QtGui.QHeaderView.Stretch)

    def setup_combo_boxes(self):
        # TODO get values from bbss package
        export_formats = ('LogoDidact', 'Radius Server', 'Active Directory')
        self.export_format_combobox.addItems(export_formats)

    def center_on_screen(self):
        """Centers the window on the screen."""
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def set_signals_and_slots(self):
        """Sets all signals and slots for main window."""
        self.import_data_button.clicked.connect(self.on_import_data)
        self.load_file_button.clicked.connect(self.on_load_file)
        self.delete_database_button.clicked.connect(self.on_delete_database)
        self.import_filter_text.textEdited.connect(self.on_import_filter)
        self.old_import_number.textEdited.connect(
            self.on_update_export_changeset)
        self.new_import_number.textEdited.connect(
            self.on_update_export_changeset)
        self.export_data_button.clicked.connect(self.on_export_data)
        self.TaskTabbedPane.currentChanged.connect(self.on_tab_changed)
        self.menu_exit.triggered.connect(self.close)

    @QtCore.pyqtSlot()
    def on_load_file(self):
        logger.info('Loading file with student data...')
        self.FILENAME = QtGui.QFileDialog\
            .getOpenFileName(self, 'Öffne Schülerdatendatei...', '',
                             'CSV-Dateien (*.csv);;Excel-Dateien (*.xls)')
        logger.info('Student data file chosen: "{0}".'.format(self.FILENAME))
        import os
        _, ext = os.path.splitext(self.FILENAME)
        if ext == '.csv':
            bbss.import_csv_file(self.FILENAME)
        elif ext == '.xls':
            bbss.import_excel_file(self.FILENAME)
        else:
            logger.warn('Given file format can not be imported.')
        self.import_table_model.update(bbss.student_list)
        self.proxy_import_table_model.setSourceModel(self.import_table_model)
        self.import_data_tableview.resizeColumnsToContents()

    @QtCore.pyqtSlot()
    def on_import_data(self):
        logger.info('Importing data into database...')
        bbss.store_students_db(self.FILENAME)
        message = "Schülerdaten aus Datei {0} wurden erfolgreich eingelesen."\
                  .format(self.FILENAME)
        QtGui.QMessageBox.information(self, 'Schülerdaten importiert.',
                                      message, QtGui.QMessageBox.Ok)

    @QtCore.pyqtSlot()
    def on_delete_database(self):
        logger.info('Deleting database file...')
        message = "Soll die Datenbankdatei wirklich gelöscht werden? "\
                  "Alle gespeicherten Informationen gehen dabei verloren!"
        reply = QtGui.QMessageBox.question(self, 'Datenbank löschen?',
                                           message, QtGui.QMessageBox.Yes,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            bbss.clear_database()

    @QtCore.pyqtSlot(str)
    def on_import_filter(self, filter_string):
        if filter_string:
            logger.debug('Filtering for {0}...'.format(filter_string))
            syntax = QtCore.QRegExp.PatternSyntax(QtCore.QRegExp.Wildcard)
            caseSensitivity = QtCore.Qt.CaseInsensitive
            regExp = QtCore.QRegExp(filter_string, caseSensitivity, syntax)
            self.proxy_import_table_model.setFilterRegExp(regExp)
            #self.proxy_import_table_model.setFilterFixedString(filter_string)
            count = self.proxy_import_table_model.rowCount()
            self.search_result_label.setText('{} Schüler gefunden...'
                                             .format(count))
        else:
            self.search_result_label.setText('')

    @QtCore.pyqtSlot()
    def on_update_export_changeset(self):
        self.update_changeset_from_database()

    def update_changeset_from_database(self):
        """Updates import IDs and changeset based on currently set values in
           user interface."""
        try:
            old_id = int(self.old_import_number.text())
        except:
            logger.warn('Import IDs must be integer values.')
            old_id = 0
        try:
            new_id = int(self.new_import_number.text())
        except:
            logger.warn('Import IDs must be integer values.')
            new_id = 0
        self.changeset = bbss.generate_changeset(old_import_id=old_id,
                                                 new_import_id=new_id)
        logger.debug('{} added, {} removed'
                     .format(len(self.changeset.students_added),
                             len(self.changeset.students_removed)))
        # update tables for added and removed students
        self.added_students_table_model = StudentTableModel(
            self.changeset.students_added)
        self.removed_students_table_model = StudentTableModel(
            self.changeset.students_removed)
        self.added_students_tableview.setModel(
            self.added_students_table_model)
        self.removed_students_tableview.setModel(
            self.removed_students_table_model)
        # update labels with student count
        self.added_student_table_label.setText('Hinzugefügte Schüler ({}):'
            .format(len(self.changeset.students_added)))
        self.removed_student_table_label.setText('Entfernte Schüler ({}):'
            .format(len(self.changeset.students_removed)))

    @QtCore.pyqtSlot()
    def on_export_data(self):
        self.update_changeset_from_database()
        export_format = self.export_format_combobox.currentText()
        export_file = self.get_filename_for_export()
        if export_file:
            if export_format == 'LogoDidact':
                bbss.export_csv_file(export_file, self.changeset)
            elif export_format == 'Radius Server':
                bbss.export_radius_file(export_file, self.changeset)
            else:
                logger.warn('Export format not yet implemented.')
                message = 'Export zu "Active Directory" noch nicht implementiert.'
                QtGui.QMessageBox.information(self, 'Fehler bei Export',
                                              message, QtGui.QMessageBox.Ok)

    def get_filename_for_export(self):
        """Gets filename for export of student data from user."""
        filename = QtGui.QFileDialog.getSaveFileName(self,
                                                     'Speichere Datei...')
        logger.info('Export file chosen: "{0}".'.format(filename))
        return filename

    @QtCore.pyqtSlot()
    def on_tab_changed(self):
        if self.TaskTabbedPane.currentIndex() == 1:
            self.update_changeset_from_database()


def start_gui():
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    main = BbssGui()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    start_gui()