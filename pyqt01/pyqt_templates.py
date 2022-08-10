import sys
from PyQt5.QtWidgets import QApplication, QWidget

# 클래스 oop
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:  # -> None return 하는 값이 없다. init은 기본적으로 None이다. - > str : string값을 return 한다.
        super().__init__()
        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(1000,300,900,700)
        self.setWindowTitle('QTemplate')
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()