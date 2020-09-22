from random import randint, choice
from pprint import pprint, pformat
from copy import deepcopy
from itertools import groupby
import settings


class Matrix(object):
    """
    TODO
    """
    def __init__(self):
        self.dimension = settings.SIZE
        self.matrix = self.add_new(self._new_matrix())
        self.operational_matrix = self.matrix
        self.is_end = False
        self.score = 0
        self._memory = [0] * settings.UNDO_BACKUP

    @property
    def memory(self):
        return self._memory

    @memory.setter
    def memory(self, value):
        self._memory = value

    @property
    def size(self):
        return self.dimension

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, value):
        self._matrix = value

    @property
    def operational_matrix(self):
        return self._operational_matrix

    @operational_matrix.setter
    def operational_matrix(self, value):
        self._operational_matrix = value

    def _new_matrix(self):
        return [[0] * self.dimension for _ in range(self.dimension)]

    def backup(self, matrix):
        """
        TODO
        :param matrix:
        :return:
        """
        for take in range(settings.UNDO_BACKUP):
            if not self.memory[take]:
                self.memory[take] = matrix
        else:
            self.memory.pop(0)
            self.memory.append(matrix)

    def undo(self):
        """
        TODO
        :return:
        """
        for idx, matrix in enumerate(reversed(self.memory)):
            if matrix:
                self.matrix = matrix
                self.matrix[settings.UNDO_BACKUP - idx - 1] = 0
                return True
        else:
            return False

    def shift(self, matrix):
        """
        TODO
        :param matrix:
        :return:
        """
        new_matrix = self._new_matrix()

        for row in range(self.dimension):
            placer = 0

            for col in range(self.dimension):

                if matrix[row][col]:
                    new_matrix[row][placer] = matrix[row][col]
                    placer += 1

        return new_matrix

    def reverse(self, matrix):
        """
        TODO
        :param matrix:
        :return:
        """
        new_matrix = self._new_matrix()

        for row in range(self.dimension):

            for col in range(self.dimension):
                new_matrix[row][col] = matrix[row][self.dimension - col - 1]

        return new_matrix

    def rotate(self, matrix):
        """
        TODO
        :param matrix:
        :return:
        """
        new_matrix = self._new_matrix()

        for row in range(self.dimension):

            for col in range(self.dimension):
                new_matrix[row][col] = matrix[col][row]

        return new_matrix

    def combine(self, matrix):
        """
        TODO
        :param matrix:
        :return:
        """
        for row in range(self.dimension):

            for col in range(self.dimension - 1):

                if matrix[row][col] and matrix[row][col] == matrix[row][col + 1]:
                    matrix[row][col] *= 2
                    matrix[row][col + 1] = 0
                    self.score += matrix[row][col]

        return matrix

    def add_new(self, matrix):
        """
        TODO
        :param matrix:
        :return:
        """
        free = [[row, col] for row in range(self.dimension) for col in range(self.dimension) if not matrix[row][col]]
        if free:
            new_number = choice([2, 2, 2, 2, 2, 2, 4])
            new_place = choice(free)
            matrix[new_place[0]][new_place[1]] = new_number
        return matrix

    def check_end(self, matrix):
        """
        TODO
        :param matrix:
        :return:
        """
        if any(2048 in row for row in matrix):
            print("You Win!!!")
            self.is_end = True
        if not any(0 in row for row in matrix):
            if not self.is_any_addable(matrix):
                print("Game over")
                self.is_end = True

    def is_any_addable(self, matrix):
        """
        TODO
        :param matrix:
        :return:
        """
        for row in range(self.dimension):
            for col in range(self.dimension - 1):
                if matrix[row][col] == matrix[row][col + 1]:
                    return True
        for row in range(self.dimension - 1):
            for col in range(self.dimension):
                if matrix[row][col] == matrix[row + 1][col]:
                    return True
        return False

    def is_valid_move(self, matrix):
        """
        TODO
        :param matrix:
        :return:
        """
        if self.is_column_filled(matrix, self.size - 1):
            for row in matrix:
                print("row:", row)
                valid_numbers = []
                for value in row:
                    if value:
                        valid_numbers.append(value)
                print ("valid_numbers: ", valid_numbers)
                print("Tst: ", len(set(valid_numbers)) , len(valid_numbers))
                if not len(list(groupby(valid_numbers))) == len(valid_numbers):

                    return True
        else:
            return True

    def is_column_filled(self, matrix, column):
        """
        TODO
        :param matrix:
        :param column:
        :return:
        """
        first_column = []
        for row in range(self.dimension):
            first_column.append(matrix[row][column])
        print("first_column ", first_column)
        if 0 not in first_column:
            return True

    def right(self):
        """
        TODO
        :return:
        """
        matrix = deepcopy(self.matrix)
        matrix = self.reverse(matrix)
        if self.is_valid_move(matrix):
            matrix = self.shift(matrix)
            matrix = self.combine(matrix)
            matrix = self.shift(matrix)
            matrix = self.reverse(matrix)
            self.check_end(matrix)
            if not self.is_end:
                matrix = self.add_new(matrix)
            self.matrix = matrix

    def left(self):
        """
        TODO
        :return:
        """
        matrix = deepcopy(self.matrix)

        if self.is_valid_move(matrix):
            matrix = self.shift(matrix)
            matrix = self.combine(matrix)
            matrix = self.shift(matrix)
            self.check_end(matrix)
            if not self.is_end:
                matrix = self.add_new(matrix)
            self.matrix = matrix

    def up(self):
        """
        TODO
        :return:
        """
        matrix = deepcopy(self.matrix)

        matrix = self.rotate(matrix)
        if self.is_valid_move(matrix):
            matrix = self.shift(matrix)
            matrix = self.combine(matrix)
            matrix = self.shift(matrix)
            matrix = self.rotate(matrix)
            self.check_end(matrix)
            if not self.is_end:
                matrix = self.add_new(matrix)
            self.matrix = matrix

    def down(self):
        """
        TODO
        :return:
        """
        matrix = deepcopy(self.matrix)

        matrix = self.rotate(matrix)
        matrix = self.reverse(matrix)
        if self.is_valid_move(matrix):
            matrix = self.shift(matrix)
            matrix = self.combine(matrix)
            matrix = self.shift(matrix)
            matrix = self.reverse(matrix)
            matrix = self.rotate(matrix)
            self.check_end(matrix)
            if not self.is_end:
                matrix = self.add_new(matrix)
            self.matrix = matrix

    def __repr__(self):
        return "{}".format(pformat(self.matrix))


if __name__ == '__main__':
    pass
    # m = Matrix()
    # print(m)
    # counter = 0
    # while not m.is_end:
    #     mode = choice(["8", "6", "4", "2"])
    #     # mode = input("Enter your move: ")
    #     if mode == "8":
    #         m.up()
    #     elif mode == "2":
    #         m.down()
    #     elif mode == "4":
    #         m.left()
    #     else:
    #         m.right()
    #     counter += 1
    #     print("Try: ", counter)
    #     print(m)
    #     print(m.score)

