from __future__ import annotations


def greatest_common_divisor(first: int, second: int) -> int:
    """
    Returns the greatest common divisor of two numbers.
    :param first: The first number.
    :param second: The second number.
    :return:
    """
    while first:
        if first < second:
            first, second = second, first
        first %= second
    return second


class Fraction:

    def __init__(self, numerator: int, denominator: int):
        """
        Initialize a Fraction. Arguments are the numerator and denominator.
        :param numerator: The numerator.
        :param denominator: The denominator.
        """
        if not denominator:
            raise ValueError

        self.numerator = numerator
        self.denominator = denominator
        self.reduce()

    def __str__(self):
        """
        Defines the string representation of the Fraction, formatted as "A / B", A being the numerator and B being the
        denominator
        :return: The string
        """
        if self.denominator == 1:
            return str(self.numerator)
        return "{} / {}".format(self.numerator, self.denominator)

    def evaluate(self) -> float:
        """
        Evaluates the Fraction.
        :return: the Float value of the Fraction.
        """
        return self.numerator / self.denominator

    def reduce(self):
        """
        Reduces the Fraction. If the fraction is negative, the numerator will be negative and the denominator positive.
        """
        factor = greatest_common_divisor(abs(self.numerator), abs(self.denominator))
        self.numerator /= factor
        self.denominator /= factor

        self.numerator = int(self.numerator)
        self.denominator = int(self.denominator)

        if self.denominator < 0:
            self.denominator *= -1
            self.numerator *= -1

    @classmethod
    def input_fraction(cls) -> Fraction:
        valid_input = False
        while not valid_input:
            value = input("Input value:")
            first = 0
            first_entered = False
            sign = 1
            second = 0
            i = 0

            while i != len(value) and value[i] == ' ':
                i += 1

            if i != len(value) and value[i] == '-':
                sign = -1
                i += 1

            while i != len(value) and value[i] == ' ':
                i += 1

            while i != len(value) and ord('0') <= ord(value[i]) <= ord('9'):
                first *= 10
                first += int(value[i])
                i += 1
                first_entered = True

            while i != len(value) and value[i] == ' ':
                i += 1

            if i == len(value) and first_entered:
                second = 1
                valid_input = True

            if i != len(value) and value[i] == '/':
                i += 1

                while i != len(value)  and value[i] == ' ':
                    i += 1

                while i != len(value) and ord('0') <= ord(value[i]) <= ord('9'):
                    second *= 10
                    second += int(value[i])
                    i += 1

                while i != len(value) and value[i] == ' ':
                    i += 1

                if i == len(value):
                    valid_input = True

            if not valid_input:
                print("Invalid input")

        return Fraction(sign * first, second)

    def __add__(self, other) -> Fraction:
        """
        Adds two Fractions or a fraction and an int together and returns the result. Overloads the binary + operator.
        :param other: The Fraction or int to be added to self.
        :return: The reduced sum.
        """
        if isinstance(other, int):
            return Fraction(self.numerator + self.denominator * other, self.denominator)

        numerator = self.numerator * other.denominator + other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __sub__(self, other) -> Fraction:
        """
        Subtracts one Fraction from another or an int from a fraction and returns the result. Overloads the binary -
        operator.
        :param other: The Fraction or int to be subtracted from self.
        :return: The reduced difference.
        """
        if isinstance(other, int):
            other = Fraction(other, 1)

        numerator = self.numerator * other.denominator - other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __mul__(self, other) -> Fraction:
        """
        Multiplies two Fractions or a Fraction and an int together. Overloads the * operator.
        :param other: The Fraction or int to be multiplied with self.
        :return: The reduced product.
        """
        if isinstance(other, int):
            return Fraction(self.numerator * other, self.denominator)

        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __truediv__(self, other) -> Fraction:
        """
        Divides a Fraction by another Fraction or an int. Overloads the / operator
        :param other: The divisor. self is the dividend.
        :return: The quotient.
        """
        if isinstance(other, int):
            return Fraction(self.numerator, self.denominator * other)

        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator
        return Fraction(numerator, denominator)

    def __pow__(self, power: int) -> Fraction:
        """
        Takes the powerth power of self. Power can be either an int or a Fraction. Overloads the ** operator.
        :param power: The power to which self is being raised.
        :return: The result. May be either a Fraction or an int.
        """
        numerator = self.numerator
        denominator = self.denominator

        if isinstance(power, int):
            if power > 0:
                return Fraction(numerator ** power, denominator ** power)
            elif power == 0:
                return Fraction(1, 1)
            return Fraction(denominator ** power, numerator ** power)
        else:
            numerator **= (1 / float(power.denominator))
            denominator **= (1 / float(power.denominator))

            numerator **= power.numerator
            denominator **= power.numerator

            if power.numerator < 0:
                return Fraction(denominator, numerator)
            return Fraction(numerator, denominator)

    def __lt__(self, other) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if self is less than other, False otherwise.
        Overloads the < operator.
        :param other: The Fraction or int to be compared with self.
        :return: True if self is less than other, False if other is less than self.
        """
        if isinstance(other, int):
            return self.numerator < self.denominator * other
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __gt__(self, other: Fraction) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if self is greater than other, False otherwise.
        Overloads the >
        operator.
        :param other: The Fraction or int to be compared with self.
        :return: True if self is greater than other, False if other is greater than self.
        """
        if isinstance(other, int):
            return self.numerator > self.denominator * other
        return self.numerator * other.denominator > other.numerator * self.denominator

    def __le__(self, other: Fraction) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if self is less than or equal to other, False
        otherwise. Overloads the >= operator.
        :param other: The Fraction or int to be compared with self.
        :return: True if self is less than or equal to other, False if other is less than self.
        """
        if isinstance(other, int):
            return self.numerator <= self.denominator * other
        return self.numerator * other.denominator <= other.numerator * self.denominator

    def __ge__(self, other: Fraction) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if self is greater than or equal to other,
        False otherwise. Overloads the >= operator.
        :param other: The Fraction or int to be compared with self.
        :return: True if self is greater than or equal to other, False if other is greater than self.
        """
        if isinstance(other, int):
            return self.numerator >= self.denominator * other
        return self.numerator * other.denominator >= other.numerator * self.denominator

    def __eq__(self, other: Fraction) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if self is equal to other, False otherwise.
        Overloads the == operator.
        :param other: The Fraction or int to be compared with self.
        :return: True if self is equal to other, False if self is not equal to other.
        """
        if isinstance(other, int):
            return self.numerator == self.denominator * other
        return self.numerator * other.denominator == other.numerator * self.denominator

    def __ne__(self, other: Fraction) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if self is not equal to other, False otherwise.
        Overloads the != operator.
        :param other: The Fraction to be compared with self.
        :return: True if self is not equal to other, False if self is equal to other.
        """
        if isinstance(other, int):
            return self.numerator != self.denominator * other
        return self.numerator * other.denominator != other.numerator * self.denominator

    def __neg__(self) -> Fraction:
        """
        Flips the sign of self. Overloads the unary - operator.
        :return: The negative of self.
        """
        return Fraction(-self.numerator, self.denominator)


class Matrix:
    def __init__(self, rows, cols):
        """
        Creates a Matrix of dimensions rows x cols.
        :param rows: The number of rows in the matrix.
        :param cols: The number of cols in the matrix.
        """
        self.rows = rows
        self.cols = cols
        self.matrix = [[0] * cols for i in range(rows)]

    def __str__(self):
        string = ''
        for i in range(self.rows):
            for j in range(self.cols):
                string += str(self.matrix[i][j]) + '\t\t\t'
            string += '\n\n'
        return string

    def store_value(self, value, row: int, col: int):
        """
        Stores a value of type int or Fraction into position row x col of the matrix.
        :param value: The value to be stored.
        :param row: The row it is to be stored in.
        :param col: The column it is to be stored in.
        """
        self.matrix[row][col] = value

    def input_matrix(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print("Value to be input in position (" + str(i + 1) + ", " + str(j + 1) + ")")
                self.matrix[i][j] = Fraction.input_fraction()


# test = Fraction.input_fraction()
# # test = Fraction(5, 1)
# # print(test)

test = Matrix(3, 3)
test.input_matrix()

print(test)

