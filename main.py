import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidgetItem
from addEditCoffeeForm import The_Other_Ui_Form
from mainform import Ui_Form


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = 'coffee.db'
        self.btn.clicked.connect(self.change_table)

    def change_table(self):
        self.change_form = addEditCoffeeForm(self, self.db)
        self.change_form.show()

    def loadUi(self):
        cur = sqlite3.connect(self.db).cursor()
        result = cur.execute("SELECT * FROM about").fetchall()
        title = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена',
                 'Объём упаковки']
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def enterEvent(self, QEvent):
        self.loadUi()


class addEditCoffeeForm(QWidget, The_Other_Ui_Form):
    def __init__(self, *db):
        super().__init__()
        self.setupUi(self)
        self.db = db[-1]
        self.loadUi()
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.save_btn.clicked.connect(self.save_table)
        self.add_btn.clicked.connect(self.add)
        self.modified = {}
        self.new = False

    def loadUi(self):
        self.con = sqlite3.connect(self.db)
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM about").fetchall()
        self.titles = ['ID', 'Название сорта', 'Степень обжарки', 'Молотый/в зернах', 'Описание вкуса', 'Цена',
                       'Объём упаковки']
        self.tableWidget.setColumnCount(len(self.titles))
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(result):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        self.modified = {}

    def item_changed(self, item):
        id = self.tableWidget.item(item.row(), 0).text()
        self.modified[(self.titles[item.column()], id)] = item.text()

    def save_table(self):
        if self.modified:
            if not self.new:
                cur = self.con.cursor()
                for key in self.modified.keys():
                    a = "UPDATE about SET\n [{}]='{}' WHERE id = {}\n"
                    cur.execute(a.format(key[0], self.modified.get(key), key[1]))
                self.con.commit()
            else:
                vals = [self.tableWidget.item(self.tableWidget.rowCount() - 1, 0).text(),
                        self.tableWidget.item(self.tableWidget.rowCount() - 1, 1).text(),
                        self.tableWidget.item(self.tableWidget.rowCount() - 1, 2).text(),
                        self.tableWidget.item(self.tableWidget.rowCount() - 1, 3).text(),
                        self.tableWidget.item(self.tableWidget.rowCount() - 1, 4).text(),
                        self.tableWidget.item(self.tableWidget.rowCount() - 1, 5).text(),
                        self.tableWidget.item(self.tableWidget.rowCount() - 1, 6).text()]
                cur = self.con.cursor()
                cur.execute("INSERT INTO about{} VALUES{}".format(tuple(self.titles), tuple(vals)))
                self.con.commit()
                self.new = False

    def add(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.new = True


if __name__ == '__main__':
    app, w = QApplication(sys.argv), MyWidget()
    w.show()
    sys.exit(app.exec())