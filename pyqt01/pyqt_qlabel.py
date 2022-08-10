import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


# 클래스 oop
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:  # -> None return 하는 값이 없다. init은 기본적으로 None이다. - > str : string값을 return 한다.
        super().__init__()
        self.initUI()

    # 화면정의를 위한 사용자 함수
    def initUI(self) -> None:
        self.addControls()
        self.setGeometry(1000,300,900,700)
        self.setWindowTitle('QLabel')
        self.show()

    def addControls(self) -> None:
        self.setWindowIcon(QIcon('./pyqt01/images/lion.png')) # 윈도우아이콘 지정
        label1 = QLabel(self)
        label2 = QLabel(self)
        label1.setStyleSheet(
           ('border-width: 3px;'
            'border-style: solid;'
            'border-color: blue;'
            'image: url(./pyqt01/images/image1.png)'
           )                
       )

        label2.setStyleSheet(
           ('border-width: 4px;'
            'border-style: dot-dot-dash;'
            'border-color: red;'
            'image: url(./pyqt01/images/image2.png)'
           )            
        )

        box = QHBoxLayout()
        box.addWidget(label1)
        box.addWidget(label2)

        self.setLayout(box)


    






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()