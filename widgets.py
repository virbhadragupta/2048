import sys
from PySide2 import QtWidgets, QtCore
import main


class Game(QtWidgets.QWidget):
    def __init__(self):
        super(Game, self).__init__()
        self.setWindowTitle("2048 Game")
        self.setGeometry(400, 400, 400, 400)
        self.matrix = main.Matrix()
        self.setup()

    def setup(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.score = QtWidgets.QLabel("Score: 0")
        self.score.setAlignment(QtCore.Qt.AlignCenter)

        self.grid = QtWidgets.QGridLayout()
        self.index_holder = [[0] * self.matrix.size for _ in range(self.matrix.size)]

        for i in range(self.matrix.size):
            for j in range(self.matrix.size):
                num = Number()
                self.index_holder[i][j] = num
                num.setGeometry(50, 50, 50, 50)
                self.grid.addWidget(num, i, j)

        self.main_layout.addWidget(self.score)
        self.main_layout.addLayout(self.grid, QtCore.Qt.AlignCenter)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self.up_move()
        elif event.key() == QtCore.Qt.Key_Down:
            self.down_move()
        elif event.key() == QtCore.Qt.Key_Right:
            self.right_move()
        elif event.key() == QtCore.Qt.Key_Left:
            self.left_move()
        elif event.key() == (QtCore.Qt.Key_Control and QtCore.Qt.Key_Z):
            self.undo()
        self.refresh()
        self.score.setText("Score: {}".format(self.matrix.score))
        event.accept()

    def undo(self):
        self.matrix.undo()

    def left_move(self):
        self.matrix.left()

    def right_move(self):
        self.matrix.right()

    def up_move(self):
        self.matrix.up()

    def down_move(self):
        self.matrix.down()

    def refresh(self):
        for row in range(self.matrix.size):
            for col in range(self.matrix.size):
                self.index_holder[row][col].setText(str(self.matrix.matrix[row][col]))


class Number(QtWidgets.QLabel):
    def __init__(self, number=""):
        super(Number, self).__init__(number)
        self.number = number
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText(self.number)

    def setText(self, text):
        text = str(text)
        super(Number, self).setText(text)
        if text == "0" or text == "":
            self.setStyleSheet("background-color: #fae0c5")
        elif text == "2":
            self.setStyleSheet("background-color: #fab670")
        elif text == "4":
            self.setStyleSheet("background-color: #b2ff7a")
        elif text == "8":
            self.setStyleSheet("background-color: #ff0000")
        elif text == "16":
            self.setStyleSheet("background-color: #7affde")
        elif text == "32":
            self.setStyleSheet("background-color: #7abaff")
        elif text == "64":
            self.setStyleSheet("background-color: #a56eff")
        elif text == "128":
            self.setStyleSheet("background-color: #e264f5")
        elif text == "256":
            self.setStyleSheet("background-color: #d13681")
        elif text == "512":
            self.setStyleSheet("background-color: #3e2c91")
        elif text == "1024":
            self.setStyleSheet("background-color: #2c751b")
        else:
            self.setStyleSheet("background-color: #f6ff00")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    instance = Game()
    instance.show()
    app.exec_()
    sys.exit(0)
