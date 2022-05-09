from PyQt6.QtGui import (QAction, QKeySequence)
from PyQt6.QtWidgets import (
    QListWidget, QPushButton, QVBoxLayout, QMainWindow, QWidget, QStackedWidget, QTabBar, QTableWidget, QHBoxLayout,
    QAbstractItemView
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Spectra Correlator")
        self.setMinimumSize(1000, 800)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        self.tab_bar = QTabBar()
        self.tab_bar.addTab("File Select")
        self.tab_bar.addTab("Results")
        self.main_layout.addWidget(self.tab_bar)

        self.stack_widget = QStackedWidget()
        self.main_layout.addWidget(self.stack_widget)

        self.import_page = QWidget()
        self.import_layout = QVBoxLayout()

        self.file_buttons = QWidget()
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 0, 0, 0)

        self.import_button = QPushButton("Import")
        self.button_layout.addWidget(self.import_button)
        self.remove_button = QPushButton("Remove")
        self.button_layout.addWidget(self.remove_button)
        self.file_buttons.setLayout(self.button_layout)
        self.import_layout.addWidget(self.file_buttons)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.import_layout.addWidget(self.file_list)

        self.calculate_button = QPushButton("Calculate")
        self.import_layout.addWidget(self.calculate_button)
        self.import_page.setLayout(self.import_layout)

        self.results_page = QWidget()
        self.results_layout = QVBoxLayout()

        self.results_table = QTableWidget()
        self.results_table.setAlternatingRowColors(True)
        self.results_layout.addWidget(self.results_table)

        self.export_button = QPushButton("Export")
        self.results_layout.addWidget(self.export_button)
        self.results_page.setLayout(self.results_layout)

        self.stack_widget.addWidget(self.import_page)
        self.stack_widget.addWidget(self.results_page)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.show()

        self.delete_action = QAction()
        self.delete_action.setShortcut(QKeySequence.StandardKey.Delete)
        self.remove_button.addAction(self.delete_action)
        self.remove_button.clicked.connect(self.delete_action.trigger)

        self.copy_action = QAction()
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.results_table.addAction(self.copy_action)
