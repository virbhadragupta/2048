from random import randint, choice
from pprint import pprint, pformat
import settings


class Matrix(object):
    def __init__(self):
        self.matrix = self._new_matrix()
        self.add_new()
        self.is_end = False
        self.score = 0

    @property
    def size(self):
        return settings.SIZE

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = value

    @staticmethod
    def _new_matrix():
        return [[0] * settings.SIZE for _ in range(settings.SIZE)]

    def shift(self):
        new_matrix = self._new_matrix()

        for row in range(settings.SIZE):
            placer = 0

            for col in range(settings.SIZE):

                if self.matrix[row][col]:
                    new_matrix[row][placer] = self.matrix[row][col]
                    placer += 1

        self.matrix = new_matrix

    def reverse(self):
        new_matrix = self._new_matrix()

        for row in range(settings.SIZE):

            for col in range(settings.SIZE):
                new_matrix[row][col] = self.matrix[row][settings.SIZE - col - 1]

        self.matrix = new_matrix

    def rotate(self):
        new_matrix = self._new_matrix()

        for row in range(settings.SIZE):

            for col in range(settings.SIZE):
                new_matrix[row][col] = self.matrix[col][row]

        self.matrix = new_matrix

    def combine(self):
        for row in range(settings.SIZE):

            for col in range(settings.SIZE - 1):

                if self.matrix[row][col] and self.matrix[row][col] == self.matrix[row][col + 1]:
                    self.matrix[row][col] *= 2
                    self.matrix[row][col + 1] = 0
                    self.score += self.matrix[row][col]

    def add_new(self):
        free = [[row, col] for row in range(settings.SIZE) for col in range(settings.SIZE) if not self.matrix[row][col]]
        if free:
            new_number = choice([2, 2, 2, 2, 2, 2, 4])
            new_place = choice(free)
            self.matrix[new_place[0]][new_place[1]] = new_number

    def check_end(self):
        if any(2048 in row for row in self.matrix):
            print("You Win!!!")
            self.is_end = True
        if not any(0 in row for row in self.matrix):
            if not self.valid_move():
                print("Game over")
                self.is_end = True

    def valid_move(self):
        for row in range(settings.SIZE):
            for col in range(settings.SIZE - 1):
                if self.matrix[row][col] == self.matrix[row][col + 1]:
                    return True
        for row in range(settings.SIZE - 1):
            for col in range(settings.SIZE):
                if self.matrix[row][col] == self.matrix[row + 1][col]:
                    return True
        return False

    def right(self):
        self.reverse()
        self.shift()
        self.combine()
        self.shift()
        self.reverse()
        self.check_end()
        if not self.is_end:
            self.add_new()

    def left(self):
        self.shift()
        self.combine()
        self.shift()
        self.check_end()
        if not self.is_end:
            self.add_new()

    def up(self):
        self.rotate()
        self.shift()
        self.combine()
        self.shift()
        self.rotate()
        self.check_end()
        if not self.is_end:
            self.add_new()

    def down(self):
        self.rotate()
        self.reverse()
        self.shift()
        self.combine()
        self.shift()
        self.reverse()
        self.rotate()
        self.check_end()
        if not self.is_end:
            self.add_new()

    def __repr__(self):
        return "{}".format(pformat(self.matrix))


if __name__ == '__main__':
    m = Matrix()
    print(m)
    counter = 0
    while not m.is_end:
        mode = choice(["8", "6", "4", "2"])
        # mode = input("Enter your move: ")
        if mode == "8":
            m.up()
        elif mode == "2":
            m.down()
        elif mode == "4":
            m.left()
        else:
            m.right()
        counter += 1
        print("Try: ", counter)
        print(m)
        print(m.score)

