import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



# 클래스 oop
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:  # -> None return 하는 값이 없다. init은 기본적으로 None이다. - > str : string값을 return 한다.
        super().__init__()
        uic.loadUi('./pyqt02/ttask.ui',self)
        self.initUI()

    def initUI(self) -> None:
        self.addControls()
        self.show()

    def addControls(self) -> None:
        self.btnStart.clicked.connect(self.btn1_clicked)  # 시그널 연결
    
    def btn1_clicked(self):
        self.txbLog.append('실행!!')
        self.pgbTask.setRange(0, 999999)
        for i in range(0, 1000000): # 응답없음 발생!!
            print(f'출력 : {i}')
            self.pgbTask.setValue(i)
            self.txbLog.append(f'출력 > {i}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()
