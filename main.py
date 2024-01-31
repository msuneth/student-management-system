import sqlite3

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QLabel, QWidget,
                             QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog,
                             QComboBox, QToolBar, QStatusBar, QMessageBox)
import sys
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(500, 500)

        # menu bar
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert_data)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        search_student_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_student_action.triggered.connect(self.search_data)
        edit_menu_item.addAction(search_student_action)

        # table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_student_action)

        # status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # detect a click on the cell
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit_record)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_record)

        children = self.statusbar.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("Select * from students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert_data(self):
        dialog = InsertDialog()
        dialog.exec()

    def search_data(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit_record(self):
        dialog = EditDialog()
        dialog.exec()

    def delete_record(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setText("This is a test on GUI usage of python")


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")
        print("delete_record")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete record?")
        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes_button, 1, 0)
        layout.addWidget(no_button, 1, 1)
        self.setLayout(layout)

        yes_button.clicked.connect(self.delete_student)

    def delete_student(self):
        # get student id
        index = main_window.table.currentRow()
        student_id = main_window.table.item(index, 0).text()

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("Delete from students where id=?",
                       (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully")
        confirmation_widget.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = main_window.table.currentRow()

        # get student id
        self.student_id = main_window.table.item(index, 0).text()

        # update student name
        student_name = main_window.table.item(index, 1).text()

        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # update subjects
        course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Astronomy", "Maths", "Biology", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # update mobile
        student_mobile = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(student_mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # submit
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("Update students  set name=?, course=?, mobile=? where id=?",
                       (name, course, mobile, self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()

        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was updated successfully")
        confirmation_widget.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # add student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # add subjects
        self.course_name = QComboBox()
        courses = ["Astronomy", "Maths", "Biology", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # add mobile
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # submit
        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("Insert into students (name, course, mobile) values (?,?,?)",
                       (name, course, mobile, self.student_))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # add student name
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # search
        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("Select * from students where name = ?",
                                (name,))
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
