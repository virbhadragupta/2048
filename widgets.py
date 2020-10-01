import os
import sys
from PySide2 import QtWidgets, QtCore, QtGui
import main


class Game(QtWidgets.QWidget):
    def __init__(self):
        super(Game, self).__init__()
        self.setWindowTitle("2048 Game")
        self.setGeometry(400, 400, 400, 400)
        self._transmitter = Transmitter()
        self.frame = Frame(self.transmitter)
        self.setup()

    @property
    def transmitter(self):
        return self._transmitter

    def setup(self):
        """
        TODO
        :return:
        """
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.score = QtWidgets.QLabel("Score: 0")
        self.setFont(QtGui.QFont("Arial", 20))

        self.setStyleSheet("background-color: #2C2A2A; color: white;")

        self.score.setAlignment(QtCore.Qt.AlignCenter)

        self.grid = QtWidgets.QGridLayout()

        for i in range(self.frame.size):
            for j in range(self.frame.size):

                self.grid.addWidget(self.frame.items[i][j], i, j)

        self.main_layout.addWidget(self.score)
        self.main_layout.addLayout(self.grid, QtCore.Qt.AlignCenter)

    def keyPressEvent(self, event):
        """
        TODO
        :param event:
        :return:
        """
        if event.key() == QtCore.Qt.Key_Up:
            # self.up_move()
            self.frame.move(Move.UP)
        elif event.key() == QtCore.Qt.Key_Down:
            # self.down_move()
            self.frame.move(Move.DOWN)
        elif event.key() == QtCore.Qt.Key_Right:
            # self.right_move()
            self.frame.move(Move.RIGHT)
        elif event.key() == QtCore.Qt.Key_Left:
            # self.left_move()
            self.frame.move(Move.LEFT)
        elif event.key() == (QtCore.Qt.Key_Control and QtCore.Qt.Key_Z):
            # self.undo()
            self.frame.move(Move.UNDO)
        # self.refresh()
        self.transmitter.SIGNAL.emit()
        self.score.setText("Score: {}".format(self.frame.matrix.score))
        event.accept()


class Number(QtWidgets.QLabel):

    def __init__(self, number):
        super(Number, self).__init__(str(number))
        self.number = number
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setGeometry(50, 50, 50, 50)
        self.setText(self.number)

    def refresh(self):
        self.setText(self.number)

    def set_font(self):
        size_map = {1: 40, 2: 36, 3: 30, 4: 26, 5: 22}
        size = size_map[len(str(self.number))] if len(str(self.number)) < 6 else 22
        self.setFont(QtGui.QFont("Arial", size))

    def setText(self, text):
        """
        TODO
        :param text:
        :return:
        """
        self.number = int(text)
        self.set_font()

        text = str(text) if text else ""
        super(Number, self).setText(text)

        if text == "0" or text == "":
            self.setStyleSheet("color: black;background-color: #fae0c5;border-radius: 10px;")
        elif text == "2":
            self.setStyleSheet("color: black;background-color: #fab670;border-radius: 10px;")
        elif text == "4":
            self.setStyleSheet("color: black;background-color: #b2ff7a;border-radius: 10px;")
        elif text == "8":
            self.setStyleSheet("color: black;background-color: #ff0000;border-radius: 10px;")
        elif text == "16":
            self.setStyleSheet("color: black;background-color: #7affde;border-radius: 10px;")
        elif text == "32":
            self.setStyleSheet("color: black;background-color: #7abaff;border-radius: 10px;")
        elif text == "64":
            self.setStyleSheet("color: black;background-color: #a56eff;border-radius: 10px;")
        elif text == "128":
            self.setStyleSheet("color: black;background-color: #e264f5;border-radius: 10px;")
        elif text == "256":
            self.setStyleSheet("color: black;background-color: #d13681;border-radius: 10px;")
        elif text == "512":
            self.setStyleSheet("color: black;background-color: #3e2c91;border-radius: 10px;")
        elif text == "1024":
            self.setStyleSheet("color: black;background-color: #2c751b;border-radius: 10px;")
        else:
            self.setStyleSheet("color: black;background-color: #f6ff00;border-radius: 10px;")


class Frame(object):
    def __init__(self, transmitter):
        self.matrix = main.Matrix()  # matrix
        self.transmitter = transmitter
        self._items = None
        self.transmitter.SIGNAL.connect(self.refresh)

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        self._matrix = matrix

    @property
    def size(self):
        return self.matrix.size

    def move(self, move):
        if move == Move.UP:
            self.matrix.up()
        elif move == Move.DOWN:
            self.matrix.down()
        elif move == Move.RIGHT:
            self.matrix.right()
        elif move == Move.LEFT:
            self.matrix.left()
        elif move == Move.UNDO:
            self.matrix.undo()

    def refresh(self):
        for row in range(self.size):
            for col in range(self.size):
                self.items[row][col].setText(self.matrix.matrix[row][col])
                self.items[row][col].refresh()

    @property
    def items(self):
        if not self._items:
            items = [[0] * self.size for _ in range(self.size)]
            for row in range(self.size):
                for col in range(self.size):
                    items[row][col] = Number(self.matrix.matrix[row][col])
            self._items = items
        return self._items


class Move:
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"
    UNDO = "undo"


class Transmitter(QtCore.QObject):
    SIGNAL = QtCore.Signal()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    instance = Game()
    instance.show()
    app.exec_()
    sys.exit(0)


