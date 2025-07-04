import sys
import random
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from project import Ui_MainWindow  # your generated UI module

# Sample data
LNames = ['Abashidze', 'Gigauri', 'Archvadze', 'Akhalaya', 'Badzaghua', 'Berianidze', 'Berishvili', 'Gventsadze']
FNames = ['Anna', 'Anuki', 'Barbare', 'Gvantsa', 'Diana', 'Eka', 'Elene', 'Veronika']
Subject = ['Basics of Programming', 'Calculus II', 'Introduction to Physics', 'Computer Skills']
Point = [str(i) for i in range(101)]
ch = random.choice

# SQLite setup
conn = sqlite3.connect("university.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        Ident INTEGER PRIMARY KEY,
        LName TEXT,
        FName TEXT,
        Subject TEXT,
        Point TEXT
    )
""")
conn.commit()

# OOP classes

class Person:
    def __init__(self, ident, fname, lname):
        self.ident = ident
        self.fname = fname
        self.lname = lname

    def __str__(self):
        return f"{self.ident}: {self.fname} {self.lname}"

class Student(Person):
    def __init__(self, ident, fname, lname, subject, point):
        super().__init__(ident, fname, lname)
        self.subject = subject
        self._point = int(point)

    def __str__(self):
        return f"{super().__str__()}, Subject: {self.subject}, Point: {self._point}"

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, value):
        val = int(value)
        if 0 <= val <= 100:
            self._point = val
        else:
            raise ValueError("Point must be between 0 and 100")

    @point.deleter
    def point(self):
        self._point = 0

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.point == other.point

    def __lt__(self, other):
        return self.point < other.point

    def __le__(self, other):
        return self.point <= other.point


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.add_records)
        self.ui.pushButton_2.clicked.connect(self.search_record)
        self.ui.pushButton_3.clicked.connect(self.update_record)
        self.ui.pushButton_4.clicked.connect(self.remove_record)
        self.ui.pushButton_5.clicked.connect(QtWidgets.QApplication.quit)

    def add_records(self):
        cursor.execute("DELETE FROM students")
        for i in range(10):
            student = Student(
                ident=i + 1,
                fname=ch(FNames),
                lname=ch(LNames),
                subject=ch(Subject),
                point=ch(Point)
            )
            cursor.execute("""
                INSERT INTO students (Ident, LName, FName, Subject, Point) VALUES (?, ?, ?, ?, ?)
            """, (student.ident, student.lname, student.fname, student.subject, student.point))
        conn.commit()
        QMessageBox.information(self, "Success", "10 random records added.")

    def search_record(self):
        query = "SELECT * FROM students WHERE 1=1"
        params = []

        id_text = self.ui.lineEdit.text().strip()
        lname = self.ui.lineEdit_2.text().strip()
        fname = self.ui.lineEdit_5.text().strip()
        subject = self.ui.lineEdit_4.text().strip()
        point = self.ui.lineEdit_3.text().strip()

        if id_text.isdigit():
            query += " AND Ident = ?"
            params.append(int(id_text))
        if lname:
            query += " AND LName LIKE ?"
            params.append(f"%{lname}%")
        if fname:
            query += " AND FName LIKE ?"
            params.append(f"%{fname}%")
        if subject:
            query += " AND Subject LIKE ?"
            params.append(f"%{subject}%")
        if point:
            query += " AND Point LIKE ?"
            params.append(f"%{point}%")

        cursor.execute(query, params)
        result = cursor.fetchone()

        if result:
            student = Student(
                ident=result[0],
                lname=result[1],
                fname=result[2],
                subject=result[3],
                point=result[4]
            )
            self.ui.lineEdit.setText(str(student.ident))
            self.ui.lineEdit_2.setText(student.lname)
            self.ui.lineEdit_5.setText(student.fname)
            self.ui.lineEdit_4.setText(student.subject)
            self.ui.lineEdit_3.setText(str(student.point))
        else:
            self.clear_inputs()
            QMessageBox.warning(self, "Not Found", "No such record found.")

    def update_record(self):
        id_text = self.ui.lineEdit.text().strip()
        if not id_text.isdigit():
            QMessageBox.warning(self, "Error", "Invalid ID.")
            return

        try:
            student = Student(
                ident=int(id_text),
                lname=self.ui.lineEdit_2.text().strip(),
                fname=self.ui.lineEdit_5.text().strip(),
                subject=self.ui.lineEdit_4.text().strip(),
                point=self.ui.lineEdit_3.text().strip()
            )
        except ValueError as ve:
            QMessageBox.warning(self, "Invalid Point", str(ve))
            return

        cursor.execute("""
            UPDATE students SET LName=?, FName=?, Subject=?, Point=? WHERE Ident=?
        """, (student.lname, student.fname, student.subject, student.point, student.ident))
        conn.commit()

        if cursor.rowcount:
            QMessageBox.information(self, "Updated", f"Record with ID {student.ident} updated.")
        else:
            QMessageBox.warning(self, "Not Found", f"No record with ID {student.ident} found.")

    def remove_record(self):
        id_text = self.ui.lineEdit.text().strip()
        if not id_text.isdigit():
            return

        ident = int(id_text)
        cursor.execute("DELETE FROM students WHERE Ident = ?", (ident,))
        conn.commit()

        if cursor.rowcount:
            self.clear_inputs()
            QMessageBox.information(self, "Deleted", f"Record with ID {ident} deleted.")
        else:
            QMessageBox.warning(self, "Not Found", f"No record with ID {ident} found.")

    def clear_inputs(self):
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_2.setText("")
        self.ui.lineEdit_5.setText("")
        self.ui.lineEdit_4.setText("")
        self.ui.lineEdit_3.setText("")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
