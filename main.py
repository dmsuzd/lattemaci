import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.cur = sqlite3.connect('coffee.sqlite').cursor()
        self.see.clicked.connect(self.load_table)
        self.add_update_btn.clicked.connect(self.add_update)

    def add_update(self):
        self.add_update_window = AddUpdateBtn(self)
        self.add_update_window.show()
    
    def load_table(self):
        self.tableWidget.verticalHeader().setVisible(False)
        self.data = self.cur.execute("Select * from coffee").fetchall()
        self.tableWidget.setColumnCount(len(self.data[0]))
        nms = []
        for i in self.cur.description:
            nms.append(i[0])
        self.tableWidget.setHorizontalHeaderLabels(nms)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


class AddUpdateBtn(QMainWindow):
    def __init__(self, parrent):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.parrent = parrent
        self.add_btn.clicked.connect(self.add_data)
        self.update_btn.clicked.connect(self.update_data)

    def get_text(self, text):
        if not text:
            raise ValueError
        text = text.split(";")
        if len(text) != 7:
            raise ValueError
        if not text[0].isdigit() or not text[-1].isdigit() or not text[-2].isdigit():
            raise ValueError
        text[0], text[-1], text[-2] = int(text[0]), int(text[-1]), int(text[-2])
        text = tuple(text)
        return text

    def add_data(self):
        self.statusBar().showMessage("")
        try:
            text = self.get_text(self.add_lineedit.text())
            queue = f"Insert Into coffee VALUES ({int(text[0])}, '{text[1]}', '{text[2]}', '{text[3]}', '{text[4]}', " \
                    f"{int(text[5])}, {int(text[6])})"
            self.parrent.cur.execute(queue)
            self.parrent.cor.commit()
            self.parrent.load_table()
        except ValueError:
            self.statusBar().showMessage("Некорректный ввод")
        except Exception as e:
            self.statusBar().showMessage(e)

    def update_data(self):
        self.statusBar().showMessage("")
        try:
            first_text = self.get_text(self.check_text_lineedit.text())
            second_text = self.get_text(self.update_lineedit.text())
            self.parrent.cur.execute(f"""Update coffee set Название_сорта = '{second_text[1]}', 
            Степень_обжарки = '{second_text[2]}', Молотый_или_в_зернах = '{second_text[3]}', 
            Описание_вкуса = '{second_text[4]}', Цена = {second_text[5]}, Объем_упаковки = {second_text[6]}
            WHERE Id = {first_text[0]} and Название_сорта = '{first_text[1]}' and 
            Степень_обжарки = '{first_text[2]}' and Молотый_или_в_зернах = '{first_text[3]}' and 
            Описание_вкуса = '{first_text[4]}' and Цена = {first_text[5]} and Объем_упаковки = {first_text[6]}""")
            self.parrent.cor.commit()
            self.parrent.load_table()
        except ValueError:
            self.statusBar().showMessage('Некорректный ввод')
        except Exception as e:
            self.statusBar().showMessage(e)


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app, w = QApplication(sys.argv), Coffee()
    w.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())