from funcions import get_wifi_params, compare_wifi_params
from time import sleep
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from det import Ui_MainWindow, MyWin


def main():
    old_data = get_wifi_params()
    i = 0
    while True:
        sleep(5)
        DETECTING_BOOL = open("BOOL", "r").read()
        if "True" in DETECTING_BOOL:
            cur_data = get_wifi_params()
            if compare_wifi_params(old_data, cur_data) in [1, 2, 3]:
                if i ==0:
                    app = QtWidgets.QApplication(sys.argv)
                    w = MyWin()
                    w.show()
                    app.exec_()
                    i += 1
                else:
                    w.show()
                    app.exec_()
            old_data = cur_data
        sleep(10)

main()
