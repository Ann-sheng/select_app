import sys
import random
import sqlite3
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from project import Ui_MainWindow

LNames = ['Abashidze', 'Gigauri', 'Archvadze', 'Akhalaya', 'Badzaghua', 'Berianidze', 'Berishvili', 'Gventsadze', 'Dalakishvili',
'Antidze', 'Gyorgadze', 'Gogaladze', 'Gotsiridze', 'Vardidze', 'Zarandia', 'Tadumadze', 'Labadze', 'Kvaratskhelia',
'Kusradze', 'Kveselava', 'Kapanadze', 'Kasradze', 'Kvinikadze', 'Kopadze', 'Kankia', 'Kordzaia', 'Mikava', 'Melia',
'Monyava', 'Niauri', 'Latsabidze', 'Mikadze', 'Nemsitsveridze', 'Maisuradze', 'Matsaberidze', 'Tsavania', 'Machaladze',
'Odisharia', 'Metreveli', 'Nefaridze', 'Modebadze', 'Marjanidze', 'Mumladze', 'Nasrashvili', 'Djanjghava', 'Mosia',
'Nozadze', 'Nutsubidze', 'Oniani', 'Okruashvili', 'Pertia', 'Razmadze', 'Revazashvili', 'Saganelidze', 'Jakhaia',
'Salukvadze', 'Samsonashvili', 'Samkharadze', 'Saralidze', 'Sartania', 'Sarishvili', 'Simonishvili', 'Skhiladze',
'Khurtsidze', 'Sikharulidze', 'Tabatadze', 'Fatsatsia', 'Filauri', 'Fukhashvili', 'Kobalia', 'Kipshidze', 'Shainidze',
'Fifia', 'Shengelia', 'Sherozia', 'Shvelidze', 'Chkheidze', 'Chaduneli', 'Chikvashvili', 'Tskitishvili', 'Chokoraya',
'Tsaguria', 'Tsertsvadze', 'Tsukhishvili', 'Dzindzibadze', 'Tsereteli', 'Tsiklauri', 'Chavchanidze', 'Chiradze', 'Chelidze',
'Chanturia', 'Siradze', 'Shonia', 'Khanjaladze', 'Kharazishvili', 'Kheladze', 'Khvingia', 'Khutishvili', 'Janelidze',
'Jokhadze']

FNames = ['Anna', 'Anuki', 'Barbare', 'Gvantsa', 'Diana', 'Eka', 'Elene', 'Veronika', 'Viktoria', 'Tatia', 'Lamzira',
'Tea', 'Tekle', 'Tiniko', 'Tamari', 'Isabella', 'Ia', 'Yamze', 'Lia', 'Lika', 'Lana', 'Marika', 'Manana',
'Maya', 'Maka', 'Mariam', 'Nana', 'Nani', 'Nata', 'Nato', 'Nino', 'Nona', 'Oliko', 'Ketevani', 'Salome',
'Sofiko', 'Nia', 'Christine', 'Shorena', 'Khatia', 'Aleko', 'Alika', 'Amiran', 'Andria', 'Archil', 'Aslan',
'Bachuk', 'Beka', 'Giga', 'Gyorgi', 'David', 'Gigi', 'Goga', 'Data', 'Erekle', 'Temur', 'Yakob', 'Ilia',
'Irakli', 'Lado', 'Lasha', 'Mikhail', 'Nika', 'Otari', 'Paata', 'Ramaz', 'Ramini', 'Rati', 'Rauli', 'Revazi',
'Roma', 'Romani', 'Sandro', 'Saba', 'Sergi', 'Simon', 'Shalva', 'Shota', 'Tsotne', 'Jaba']

Subject = ['Basics of Programming', 'Calculus II', 'Introduction to Physics', 'Computer Skills',
'Introduction to Chemistry', 'Introduction to Biology', 'Algorithms I', 'Introduction to Electronics',
'Data Structures', 'Algorithms II']

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
            cursor.execute("""
                INSERT INTO students (Ident, LName, FName, Subject, Point) VALUES (?, ?, ?, ?, ?)
            """, (i + 1, ch(LNames), ch(FNames), ch(Subject), ch(Point)))
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
            self.ui.lineEdit.setText(str(result[0]))
            self.ui.lineEdit_2.setText(result[1])
            self.ui.lineEdit_5.setText(result[2])
            self.ui.lineEdit_4.setText(result[3])
            self.ui.lineEdit_3.setText(result[4])
        else:
            self.ui.lineEdit.setText("")
            self.ui.lineEdit_2.setText("")
            self.ui.lineEdit_5.setText("")
            self.ui.lineEdit_4.setText("")
            self.ui.lineEdit_3.setText("")
            QMessageBox.warning(self, "Not Found", "No such Record found.")

    def update_record(self):
        id_text = self.ui.lineEdit.text().strip()

        if not id_text.isdigit():
            QMessageBox.warning(self, "Error", "Invalid ID.")
            return

        ident = int(id_text)
        lname = self.ui.lineEdit_2.text().strip()
        fname = self.ui.lineEdit_5.text().strip()
        subject = self.ui.lineEdit_4.text().strip()
        point = self.ui.lineEdit_3.text().strip()

        cursor.execute("""
            UPDATE students SET LName = ?, FName = ?, Subject = ?, Point = ? WHERE Ident = ?
        """, (lname, fname, subject, point, ident))
        conn.commit()

        if cursor.rowcount:
            QMessageBox.information(self, "Updated", f"Record with ID {ident} updated.")
        else:
            QMessageBox.warning(self, "Not Found", f"No record with ID {ident} found.")

    def remove_record(self):
        id_text = self.ui.lineEdit.text().strip()

        if not id_text.isdigit():
            return

        ident = int(id_text)
        cursor.execute("DELETE FROM students WHERE Ident = ?", (ident,))
        conn.commit()

        if cursor.rowcount:
            self.ui.lineEdit.setText("")
            self.ui.lineEdit_2.setText("")
            self.ui.lineEdit_5.setText("")
            self.ui.lineEdit_4.setText("")
            self.ui.lineEdit_3.setText("")
            QMessageBox.information(self, "Deleted", f"Record with ID {ident} deleted.")
        else:
            QMessageBox.warning(self, "Not Found", f"No record with ID {ident} found.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
