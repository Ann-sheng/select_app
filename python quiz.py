import sys
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from pymongo import MongoClient
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

client = MongoClient("mongodb://localhost:27017/")
db = client["university"]
collection = db["students"]

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
        collection.delete_many({})
        for i in range(10):
            record = {
                "Ident": i + 1,
                "LName": ch(LNames),
                "FName": ch(FNames),
                "Subject": ch(Subject),
                "Point": ch(Point)
            }
            collection.insert_one(record)
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
            self.ui.lineEdit.setText(str(r.get("Ident", "")))
            self.ui.lineEdit_2.setText(r.get("LName", ""))
            self.ui.lineEdit_5.setText(r.get("FName", ""))
            self.ui.lineEdit_4.setText(r.get("Subject", ""))
            self.ui.lineEdit_3.setText(r.get("Point", ""))
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
            QMessageBox.information(self, "Not Found", f"Record with ID {ident} Not Found.")

        ident = int(id_text)
        new_data = {
            "LName": self.ui.lineEdit_2.text().strip(),
            "FName": self.ui.lineEdit_5.text().strip(),
            "Subject": self.ui.lineEdit_4.text().strip(),
            "Point": self.ui.lineEdit_3.text().strip()
        }

        result = collection.update_one({"Ident": ident}, {"$set": new_data})

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
