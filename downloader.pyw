import sys
from PyQt5 import QtWidgets
from my_ui import Ui_Form
import tools as ts

class mywin(QtWidgets.QWidget):
    def __init__(self:None) -> None:

        """
        connecting buttons to functions, simple initialization
        """

        super(mywin, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.search)
        self.ui.pushButton_2.clicked.connect(self.download)
        self.ui.pushButton_3.clicked.connect(self.getDir)
        self.ui.tableWidget.setColumnCount(2)

        self.setWindowTitle('Music downloader')

        for i in range(50):
            chkbox = QtWidgets.QCheckBox()
            self.ui.tableWidget.setCellWidget(i, 0, chkbox)

        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        self.my_req = None

    def search(self:None) -> None:
        """
        function for searchline, makes request and filling the table
        """
        req = ts.make_con(self.ui.lineEdit.text())
        row = 0
        for i in ts.find_track(req):
            cell = QtWidgets.QTableWidgetItem(i)
            self.ui.tableWidget.setItem(row, 1, cell)
            row += 1

        self.my_req = req

    def getDir(self):
        """
        change directory
        """
        return QtWidgets.QFileDialog.getExistingDirectory(self)

    def check_colbox(self):
        """
        checking boxes and returning tuple
        """
        return (True if self.ui.tableWidget.cellWidget(i, 0).checkState() == 2 else False for i in range(50))

    def download(self):
        """
        When calling - uses func "getDir" for matching working directory
        searching matched sounds and downloads their with same name
        """

        path = self.getDir()

        for i, elem in enumerate(self.check_colbox()):

            if elem:
                filename = self.ui.tableWidget.item(i, 1).text()
                ts.save_file(filename, path, self.my_req, i)

#standart init
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    applic = mywin()
    applic.show()
    sys.exit(app.exec_())
