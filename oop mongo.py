import sys
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from pymongo import MongoClient
from project import Ui_MainWindow  # make sure this is generated from Qt Designer

# ========== DATA SOURCES ==========
LNames = ['Abashidze', 'Gigauri', 'Archvadze', 'Akhalaya', 'Badzaghua', 'Berianidze', 'Berishvili', 'Gventsadze']
FNames = ['Anna', 'Anuki', 'Barbare', 'Gvantsa', 'Diana', 'Eka', 'Elene', 'Veronika']
Subjects = ['Basics of Programming', 'Calculus II', 'Physics', 'Electronics']
Points = [str(i) for i in range(101)]
ch = random.choice

# ========== MONGODB SETUP ==========
client = MongoClient("mongodb://localhost:27017/")
db = client["university"]
collection = db["students"]

# ========== OOP CLASSES ==========

class Person:
    def __init__(self, ident, fname, lname):
        self.ident = ident
        self.fname = fname
        self.lname = lname

    def __str__(self):
        return f"{self.ident} - {self.fname} {self.lname}"

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
        if 0 <= int(value) <= 100:
            self._point = int(value)
        else:
            raise ValueError("Point must be between 0 and 100")

    @point.deleter
    def point(self):
        self._point = 0

    def __eq__(self, other):
        return self.point == other.point

    def __lt__(self, other):
        return self.point < other.point

    def __le__(self, other):
        return self.point <= other.point


# ========== MAIN APPLICATION ==========

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.add_records)       # Add
        self.ui.pushButton_2.clicked.connect(self.search_record)   # Search
        self.ui.pushButton_3.clicked.connect(self.update_record)   # Update
        self.ui.pushButton_4.clicked.connect(self.remove_record)   # Remove
        self.ui.pushButton_5.clicked.connect(QtWidgets.QApplication.quit)  # Exit

    def add_records(self):
        collection.delete_many({})
        for i in range(10):
            student = Student(
                ident=i + 1,
                fname=ch(FNames),
                lname=ch(LNames),
                subject=ch(Subjects),
                point=ch(Points)
            )
            collection.insert_one({
                "Ident": student.ident,
                "FName": student.fname,
                "LName": student.lname,
                "Subject": student.subject,
                "Point": student.point
            })
        QMessageBox.information(self, "Success", "10 random records added.")

    def search_record(self):
        id_text = self.ui.lineEdit.text().strip()
        lname = self.ui.lineEdit_2.text().strip()
        fname = self.ui.lineEdit_5.text().strip()
        subject = self.ui.lineEdit_4.text().strip()
        point = self.ui.lineEdit_3.text().strip()

        query = {}
        if id_text.isdigit():
            query["Ident"] = int(id_text)
        if lname:
            query["LName"] = {"$regex": lname, "$options": "i"}
        if fname:
            query["FName"] = {"$regex": fname, "$options": "i"}
        if subject:
            query["Subject"] = {"$regex": subject, "$options": "i"}
        if point:
            query["Point"] = {"$regex": point, "$options": "i"}

        if not query:
            return

        results = list(collection.find(query))

        if results:
            r = results[0]
            student = Student(
                ident=r.get("Ident", ""),
                fname=r.get("FName", ""),
                lname=r.get("LName", ""),
                subject=r.get("Subject", ""),
                point=r.get("Point", 0)
            )
            self.ui.lineEdit.setText(str(student.ident))
            self.ui.lineEdit_2.setText(student.lname)
            self.ui.lineEdit_5.setText(student.fname)
            self.ui.lineEdit_4.setText(student.subject)
            self.ui.lineEdit_3.setText(str(student.point))
        else:
            self.clear_inputs()
            QMessageBox.warning(self, "Not Found", "No matching record found.")

    def update_record(self):
        id_text = self.ui.lineEdit.text().strip()
        if not id_text.isdigit():
            QMessageBox.warning(self, "Error", "Invalid ID.")
            return

        ident = int(id_text)
        try:
            student = Student(
                ident=ident,
                fname=self.ui.lineEdit_5.text().strip(),
                lname=self.ui.lineEdit_2.text().strip(),
                subject=self.ui.lineEdit_4.text().strip(),
                point=self.ui.lineEdit_3.text().strip()
            )
        except ValueError as ve:
            QMessageBox.warning(self, "Invalid Point", str(ve))
            return

        result = collection.update_one({"Ident": ident}, {"$set": {
            "FName": student.fname,
            "LName": student.lname,
            "Subject": student.subject,
            "Point": student.point
        }})

        if result.matched_count:
            QMessageBox.information(self, "Updated", f"Record with ID {ident} updated.")
        else:
            QMessageBox.warning(self, "Not Found", f"No record with ID {ident} found.")

    def remove_record(self):
        id_text = self.ui.lineEdit.text().strip()
        if not id_text.isdigit():
            return

        ident = int(id_text)
        result = collection.delete_one({"Ident": ident})

        if result.deleted_count:
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


# ========== ENTRY POINT ==========
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
