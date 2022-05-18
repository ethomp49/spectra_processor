import sys

from PyQt6.QtWidgets import QApplication, QFileDialog, QTableWidgetItem
from PyQt6.QtCore import Qt

from gui import *
from spectra_correlator import *

# ===================================================
# Instantiate gui
# ===================================================

app = QApplication(sys.argv)
w = MainWindow()
lib = Library()
clipboard = app.clipboard()


def tab_changed(index):
    w.stack_widget.setCurrentIndex(index)


def import_button_clicked():
    file_list = w.import_page.file_list
    file_dialog = QFileDialog()
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)

    files = \
        file_dialog.getOpenFileNames(w, "Select files to import", 'T:/RNDData/RNDBioChem/Spectral Data',
                                     'CSV Files (*.csv)')[0]
    lib.files_import(files)

    file_list.clear()
    for file in sorted(list(lib.spectra_files.keys())):
        file_list.addItem(file)


def calculate_button_clicked():
    m = Matrix(lib)
    results = w.results_page.results_table

    size = len(m.corr_matrix)
    results.setRowCount(size)
    results.setColumnCount(size)
    filenames = sorted(list(lib.spectra_files.keys()))

    results.setHorizontalHeaderLabels(filenames)
    results.setVerticalHeaderLabels(filenames)

    for i in range(0, size):
        for j in range(0, size):
            new_item = QTableWidgetItem()
            new_item.setText(str("%.2f" % m.corr_matrix[i][j]))
            new_item.setFlags(Qt.ItemFlag(33))
            results.setItem(i, j, new_item)

    results.resizeColumnsToContents()
    w.stack_widget.setCurrentIndex(1)
    w.tab_bar.setCurrentIndex(1)


def del_triggered():
    file_list = w.import_page.file_list
    selected_files = sorted(file_list.selectedIndexes())

    for index in selected_files[::-1]:
        del lib.spectra_files[index.data()]
        file_list.takeItem(index.row())


def copy_triggered():
    results_table = w.results_page.results_table
    selected = results_table.selectedRanges()[0]
    data = ''

    for row in range(selected.topRow(), selected.bottomRow() + 1):
        for col in range(selected.leftColumn(), selected.rightColumn()):
            data += results_table.item(row, col).data(0) + '\t'
        data += results_table.item(row, selected.rightColumn()).data(0) + '\n'

    clipboard.setText(data)


def export_button_clicked():
    results_table = w.results_page.results_table
    file_dialog = QFileDialog()
    file = file_dialog.getSaveFileName(w, "Save data to:", 'T:/RNDData/RNDBioChem/Spectral Data', 'CSV File (*.csv)')[0]

    try:
        with open(file, 'w', newline='') as f:
            writer = csv.writer(f, dialect='excel')
            rows = results_table.rowCount()
            columns = results_table.columnCount()

            table = []
            header_row = ['']
            for col in range(0, columns):
                header_row.append(results_table.horizontalHeaderItem(col).data(0))
            table.append(header_row)

            for row in range(0, rows):
                new_row = [results_table.verticalHeaderItem(row).data(0)]

                for col in range(0, columns):
                    new_row.append(results_table.item(row, col).data(0))

                table.append(new_row)

            writer.writerows(table)
            pass
    finally:
        pass


# ===================================================
# Connect signals to sockets
# ===================================================
w.tab_bar.tabBarClicked.connect(tab_changed)

w.import_page.import_button.clicked.connect(import_button_clicked)

w.import_page.calculate_button.clicked.connect(calculate_button_clicked)

w.import_page.delete_action.triggered.connect(del_triggered)

w.results_page.copy_action.triggered.connect(copy_triggered)

w.results_page.export_button.clicked.connect(export_button_clicked)

# ===================================================
# Run the application
# ===================================================

app.exec()
