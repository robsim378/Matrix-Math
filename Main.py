from __future__ import annotations


def gcd(first: int, second: int) -> int:
    """
    Returns the greatest common divisor of two numbers.
    :param first: The first number.
    :param second: The second number.
    :return:
    """
    while first:    #Euclid's algorithm
        if first < second:
            first, second = second, first
        first %= second
    return second


class Fraction:
    """
    Defines fractions and several operations associated with them. All methods
    return reduced fractions or reduce self, so fractions will always be in
    their reduced forms.
    """
    def __init__(self, numerator: int, denominator: int):
        """
        Initialize a Fraction. Arguments are the numerator and denominator.
        :param numerator: The numerator.
        :param denominator: The denominator.
        """

        # Ensures both numerator and denominator are ints.
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError

        # Ensures denominator is not zero.
        if not denominator:
            raise ValueError

        self.numerator = numerator
        self.denominator = denominator
        self.reduce()

    def __str__(self):
        """
        Defines the string representation of the Fraction, formatted as
        "A / B", A being the numerator and B being the denominator
        :return: The string representation of the Fraction.
        """

        # If the fraction reduces to an integer, the denominator and fraction
        # line will not be displayed.
        if self.denominator == 1:
            return str(self.numerator)
        return "{}/{}".format(self.numerator, self.denominator)

    def __bool__(self):
        """
        Defines the boolean value for Fractions. If the numerator is zero,
        returns False. Otherwise, returns True.
        :return: True if numerator is nonzero, False if it is zero.
        """
        return bool(self.numerator)

    def evaluate(self) -> float:
        """
        Evaluates the Fraction. Returns the int value of the Fraction if it
        exists, or the float value if not.
        :return: the int or Float value of the Fraction.
        """
        if self.denominator == 1:
            return self.numerator
        return self.numerator / self.denominator

    def reduce(self):
        """
        Reduces the Fraction. If the fraction is negative, the numerator will
        be negative and the denominator positive.
        """

        divisor = gcd(abs(self.numerator), abs(self.denominator))
        self.numerator /= divisor
        self.denominator /= divisor

        self.numerator = int(self.numerator)
        self.denominator = int(self.denominator)

        # Ensures the numerator carries the sign of the Fraction.
        if self.denominator < 0:
            self.denominator *= -1
            self.numerator *= -1

    @classmethod
    def input_fraction(cls) -> Fraction:
        """
        Allows the user to input a Fraction in the form "<sign><numerator> /
        <denominator>". Whitespace is ignored.
        :return: The Fraction the user input.
        """

        # Loops until the user inputs a valid Fraction.
        valid_input = False
        while not valid_input:
            value = input("Input value:")
            numerator_imput = 0
            first_entered = False
            sign = 1
            denominator_input = 0
            i = 0

            # Skips all spaces at the start of the input, if any.
            while i != len(value) and value[i] == ' ':
                i += 1

            # Checks if the input is negative and sets sign to -1 if so.
            if i != len(value) and value[i] == '-':
                sign = -1
                i += 1

            while i != len(value) and value[i] == ' ':
                i += 1

            # For every digit in the numerator, multiplies the value of
            # numerator_input by 10 and adds another digit.
            while i != len(value) and ord('0') <= ord(value[i]) <= ord('9'):
                numerator_imput *= 10
                numerator_imput += int(value[i])
                i += 1
                first_entered = True

            while i != len(value) and value[i] == ' ':
                i += 1

            # If the user input an integer rather than a fraction, sets the
            # denominator to 1 and sets valid_input to True to end the loop.
            if i == len(value) and first_entered:
                denominator_input = 1
                valid_input = True

            # If the user input a fraction, continues parsing the string.
            if i != len(value) and value[i] == '/':
                i += 1

                while i != len(value)  and value[i] == ' ':
                    i += 1

                while i != len(value) and ord('0') <= ord(value[i]) <= ord('9'):
                    denominator_input *= 10
                    denominator_input += int(value[i])
                    i += 1

                while i != len(value) and value[i] == ' ':
                    i += 1

                if i == len(value):
                    valid_input = True

            if not valid_input:
                print("Invalid input")

        return Fraction(sign * numerator_imput, denominator_input)

    def __add__(self, other) -> Fraction:
        """
        Adds two Fractions or a fraction and an int together and returns the
        result. Overloads the binary + operator.
        :param other: The Fraction or int to be added to self.
        :return: The reduced sum.
        """

        # Special case if other is an int.
        if isinstance(other, int):
            return Fraction(self.numerator + self.denominator * other,
                            self.denominator)

        # Ensures that other is a valid type.
        if not isinstance(other, Fraction):
            raise TypeError

        numerator = self.numerator * other.denominator + \
                    other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __radd__(self, other):
        """
        Allows for the overloaded + operator from __add__ to be commutative in
        all cases where it is allowed. Same parameters as __add__.
        """
        return self.__add__(other)

    def __sub__(self, other) -> Fraction:
        """
        Subtracts one Fraction from another or an int from a fraction and
        returns the result. Overloads the binary - operator.
        :param other: The Fraction or int to be subtracted from self.
        :return: The reduced difference.
        """

        # Special case if other is an int.
        if isinstance(other, int):
            return Fraction(self.numerator - self.denominator * other,
                            self.denominator)

        # Ensures that other is a valid type.
        if not isinstance(other, Fraction):
            raise TypeError

        numerator = self.numerator * other.denominator - \
                    other.numerator * self.denominator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __rsub__(self, other):
        """
        Allows for the overloaded - operator from __sub__ to be commutative in
        all cases where it is allowed. Same parameters as __sub__.
        """

        other = Fraction(other, 1)
        return other.__sub__(self)

    def __mul__(self, other) -> Fraction:
        """
        Multiplies two Fractions or a Fraction and an int together. Overloads
        the * operator.
        :param other: The Fraction or int to be multiplied with self.
        :return: The reduced product.
        """

        # Special case if other is an int.
        if isinstance(other, int):
            return Fraction(self.numerator * other, self.denominator)

        # Ensures that other is a valid type.
        if not isinstance(other, Fraction):
            raise TypeError

        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __rmul__(self, other):
        """
        Allows for the overloaded * operator from __mul__ to be commutative in
        all cases where it is allowed. Same parameters as __mul__.
        """
        return self.__mul__(other)

    def __truediv__(self, other) -> Fraction:
        """
        Divides a Fraction by another Fraction or an int. Overloads the /
        operator.
        :param other: The divisor. self is the dividend.
        :return: The quotient.
        """

        # Special case if other is an int.
        if isinstance(other, int):
            return Fraction(self.numerator, self.denominator * other)

        # Ensures that other is a valid type.
        if not isinstance(other, Fraction):
            raise TypeError

        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator
        return Fraction(numerator, denominator)

    def __rtruediv__(self, other):
        """
        Allows for the overloaded / operator from __truediv__ to be commutative
        in all cases where it is allowed. Same parameters as __truediv__.
        """

        other = Fraction(other, 1)
        return other.__truediv__(self)

    def __pow__(self, power) -> Fraction:
        """
        Takes the powerth power of self. Power can be either an int or a
        Fraction. Overloads the ** operator.
        :param power: The power to which self is being raised.
        :return: The result. May be either a Fraction or an int.
        """

        numerator = self.numerator
        denominator = self.denominator

        # Special case if power is an int.
        if isinstance(power, int):
            if power > 0:
                return Fraction(numerator ** power, denominator ** power)
            elif power == 0:
                return Fraction(1, 1)
            return Fraction(denominator ** power, numerator ** power)

        # Ensures power is a valid type.
        if not isinstance(power, Fraction):
            raise TypeError

        numerator **= (1 / float(power.denominator))
        denominator **= (1 / float(power.denominator))

        numerator **= power.numerator
        denominator **= power.numerator

        if power.numerator < 0:
            return Fraction(int(denominator), int(numerator))
        return Fraction(int(numerator), int(denominator))

    def __rpow__(self, other):
        """
        Allows for the overloaded ** operator from __pow__ to be commutative in
        all cases where it is allowed. Same parameters as __pow__.
        """
        other = Fraction(other, 1)
        return other.__pow__(self)

    def __lt__(self, other) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if
        self is less than other, False otherwise. Overloads the < operator.
        :param other: The Fraction or int to be compared with self.
        :return: True if self is less than other, False otherwise.
        """

        # Special case if other is an int
        if isinstance(other, int):
            return self.numerator < self.denominator * other

        # Ensures that other is a valid type.
        if not isinstance(other, Fraction):
            raise TypeError

        return self.numerator * other.denominator < \
               other.numerator * self.denominator

    def __gt__(self, other: Fraction) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if
        self is greater than other, False otherwise. Overloads the > operator.
        :param other: The Fraction or int to be compared with self.
        :return: True if self is greater than other, False if other is greater
        than self.
        """

        # Special case if other is an int
        if isinstance(other, int):
            return self.numerator > self.denominator * other

        # Ensures that other is a valid type.
        if not isinstance(other, Fraction):
            raise TypeError

        return self.numerator * other.denominator > \
               other.numerator * self.denominator

    def __le__(self, other: Fraction) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if
        self is less than or equal to other, False otherwise. Overloads the >=
        operator.
        :param other: The Fraction or int to be compared with self.
        :return: True if self is less than or equal to other, False if other is
        less than self.
        """

        # Special case if other is an int
        if isinstance(other, int):
            return self.numerator <= self.denominator * other

        # Ensures that other is a valid type.
        if not isinstance(other, Fraction):
            raise TypeError

        return self.numerator * other.denominator <= \
               other.numerator * self.denominator

    def __ge__(self, other: Fraction) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if
        self is greater than or equal to other, False otherwise. Overloads the
        >= operator.
        :param other: The Fraction or int to be compared with self.
        :return: True if self is greater than or equal to other, False if other
        is greater than self.
        """

        # Special case if other is an int
        if isinstance(other, int):
            return self.numerator >= self.denominator * other

        # Ensures that other is a valid type.
        if not isinstance(other, Fraction):
            raise TypeError

        return self.numerator * other.denominator >= \
               other.numerator * self.denominator

    def __eq__(self, other: Fraction) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if
        self is equal to other, False otherwise. Overloads the == operator.
        :param other: The Fraction or int to be compared with self.
        :return: True if self is equal to other, False if self is not equal to
        other.
        """

        # Special case if other is an int
        if isinstance(other, int):
            return self.numerator == self.denominator * other

        # Ensures that other is a valid type.
        if not isinstance(other, Fraction):
            raise TypeError

        return self.numerator * other.denominator == \
               other.numerator * self.denominator

    def __ne__(self, other: Fraction) -> bool:
        """
        Compares two Fractions or a Fraction and an int and returns True if
        self is not equal to other, False otherwise. Overloads the != operator.
        :param other: The Fraction to be compared with self.
        :return: True if self is not equal to other, False if self is equal to
        other.
        """

        # Special case if other is an int
        if isinstance(other, int):
            return self.numerator != self.denominator * other

        # Ensures that other is a valid type.
        if not isinstance(other, Fraction):
            raise TypeError

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

        # Ensures that rows and cols are both ints.
        if not isinstance(rows, int) or not isinstance(cols, int):
            raise TypeError

        # Ensures that the number of rows and cols is positive.
        if rows <= 0 or cols <= 0:
            raise ValueError

        self.rows = rows
        self.cols = cols
        self.matrix = [[0] * cols for i in range(rows)]

    def __str__(self):
        """
        Defines the string representation of a Matrix.
        :return: The string representation of self.
        """

        string = ''
        for i in range(self.rows):
            for j in range(self.cols):
                string += '{:^10}'.format(str(self.matrix[i][j]))
            string += '\n\n'
        return string

    def copy_matrix(self) -> Matrix:
        """
        Returns a copy of self that is not stored at the same address and can
        be changed without impacting self.
        :return: The copy of self.
        """

        result = Matrix(self.rows, self.cols)
        result.matrix = [i[:] for i in self.matrix]
        return result

    def add_to_entry(self, other, row: int, col: int) -> Matrix:
        """
        Adds other, which must be either an int or a Fraction, to
        self.matrix[row][col].
        :param other: The int or Fraction to be added to an entry in self.
        :param row: The row of the entry to be added to.
        :param col: the column of the entry to be added to.
        :return: The Matrix with the changed entry
        """

        # Ensures that other is a valid type.
        if not isinstance(other, int) and not isinstance(other, Fraction):
            raise TypeError

        # Special case if other is an int.
        if isinstance(other, int):
            other = Fraction(other, 1)


        result = self.copy_matrix()
        result.matrix[row - 1][col - 1] += other
        return result

    def __add__(self, other: Matrix) -> Matrix:
        """
        Adds two Matrices together. Dimensions of Matrices must be the same.
        Overrides the binary + operator.
        :param other: The Matrix to be added to self.
        :return: The sum of the two Matrices.
        """

        # Ensures that other is a valid type.
        if isinstance(other, int):
            raise TypeError

        # Ensures that the two Matrices have the same dimensions.
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError

        result = Matrix(self.rows, self.cols)

        for i in range(self.rows):
            for j in range(self.cols):
                result.matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]
        return result

    def __mul__(self, other) -> Matrix:
        """
        Multiplies two Matrices. or a matrix and an int. If two Matrices,
        self.cols must be equal to other.rows. Overrides the * operator.
        :param other: The Matrix to be multiplied with self.
        :return: The product of self and other.
        """

        # Special case if other is an int.
        if isinstance(other, int):
            result = Matrix(self.rows, self.cols)
            for i in range(self.rows):
                for j in range(self.cols):
                    result.matrix[i][j] = self.matrix[i][j] * other
            return result

        # Ensures that the two Matrices are possible to multiply.
        if self.cols != other.rows:
            raise ValueError

        result = Matrix(self.rows, other.cols)

        for row in range(self.rows):
            for col in range(other.cols):
                result.matrix[row][col] = 0
                for i in range(self.cols):
                    result.matrix[row][col] += \
                    self.matrix[row][i] * other.matrix[i][col]

        return result

    def __rmul__(self, other):
        """
        Allows for the overloaded * operator from __mul__ to be commutative in
        all cases where it is allowed. Same parameters as __mul__.
        """
        return self.__mul__(other)

    def swap_rows(self, first_row, second_row) -> Matrix:
        """
        Swaps two rows in self. One of the three elementary row operations.
        :param first_row: One of the rows being swapped.
        :param second_row: The other row being swapped.
        """

        # Ensures that both rows are valid types.
        if not isinstance(first_row, int) or not isinstance(second_row, int):
            raise TypeError

        # Ensures that both rows are positive
        if first_row <= 0 or second_row <= 0:
            raise ValueError

        result = self.copy_matrix()

        for col in range(self.cols):
            result.matrix[first_row - 1][col], result.matrix[second_row - 1][col] = \
                result.matrix[second_row - 1][col], result.matrix[first_row - 1][col]
        return result

    def add_row(self, first_row: int, factor, second_row: int) -> Matrix:
        """
        Adds the elements of the second_row row of self multiplied by factor to
        the elements of the first_row row. One of the three elementary row
        operations.
        :param first_row: The row that is being changed.
        :param factor: The factor that the elements of second_row are being
        multiplied by.
        :param second_row: The row that is being added to first_row
        :return: The resulting Matrix.
        """

        # Ensures that all parameters are valid types.
        if not isinstance(first_row, int) or not isinstance(second_row, int) \
           or not isinstance(factor, int) and not isinstance(factor, Fraction):
            raise TypeError

        # Ensures that both rows are positive.
        if first_row <= 0 or second_row <= 0:
            raise ValueError

        result = self.copy_matrix()
        for col in range(self.cols):
            result.matrix[first_row - 1][col] += \
                self.matrix[second_row - 1][col] * factor
        return result

    def multiply_row(self, row: int, factor) -> Matrix:
        """
        Multiplies all the elements in a given row by factor, which can be a
        Fraction or an int. One of the three elementary row operations.
        :param row: The row to be multiplied.
        :param factor: The factor to multiply all elements by.
        :return: The resulting Matrix.
        """

        # Ensures that row and factor are valid types.
        if not isinstance(row, int) or not isinstance(factor, Fraction) \
                and not isinstance(factor, int):
            raise TypeError

        # Ensures that row is positive.
        if row <= 0:
            raise ValueError

        result = self.copy_matrix()

        for i in range(self.cols):
            result.matrix[row - 1][i] *= factor

        return result

    def gaussian_elimination(self, stop_early: bool) -> Matrix:
        """
        Returns either the row echelon form or the reduced row echelon form
        resulting from Gauss-Jordan elimination on self. If stop_early is True,
        the function will return the row echelon form if the leading entry in
        any row is in the last column (indicating no solutions to a linear
        system.) In all other cases, it will return the reduced row echelon
        form matrix.
        :param stop_early: Whether or not the algorithm stops after determining
        the row echelon form.
        :return: The resulting Matrix.
        """

        result = self.copy_matrix()
        col = 0
        row = 0

        while col < result.cols and row < result.rows:
            # Finds the first row in the current column with a leading entry.
            row_search = row
            while row_search < result.rows \
                    and not result.matrix[row_search][col]:
                row_search += 1

            # Swaps the first row with the first row containing a leading
            # entry to create a pivot.
            if row_search != row and row_search != result.rows:
                result = result.swap_rows(row + 1, row_search + 1)

            # If there is now a leading entry, sets it to 1 to serve as the
            # pivot by dividing the entire row by the leading entry.
            if result.matrix[row][col]:
                result = result.multiply_row(row + 1, 1 / result.matrix[row][col])

            # Eliminates all leading entries below the pivot by subtracting the
            # appropriate amount of the leading entry's row.
            for i in range(row + 1, result.rows):
                if result.matrix[i][col]:
                    result = result.add_row(i + 1, -result.matrix[i][col], row + 1)

            col += 1

            # If a pivot was found in the column, increases row.
            if row_search != result.rows:
                row += 1

        # If stop_early is True, checks if the Matrix has no solution. If so,
        # returns the Matrix early without computing the reduced echelon form.
        if stop_early:
            col = -1
            row = -1

            # Searches for the last row to contain an entry in the last column.
            while row >= -result.rows and not result.matrix[row][col]:
                row -= 1

            # Checks if the entry in that row is a leading entry.
            while col >= -result.cols:
                if not result.matrix[row][col - 1]:
                    return result
                col -= 1

        row = 0
        col = 1

        # Eliminates all entries above the leading entries in order to reduce
        # the Matrix to reduced row echelon form.
        while row < result.rows - 1 and col < result.cols:
            while col < result.cols - 1 and not result.matrix[row + 1][col]:
                col += 1

            for i in range(row + 1):
                result = result.add_row(i + 1, -result.matrix[i][col], row + 2)

            row += 1
            col += 1

        return result

    def find_solution(self):
        """
        Finds the solution for the system of linear equations defined by the
        Matrix self. Returns None if no solution, an n x 1 matrix for just one
        solution with n being the number of variables, and a list if there are
        infinite solutions. The list consists of m lists containing the names
        of the independent variables and the vectors associated with them,
        written as 1 x n Matrices, where m is the number of variables. The last
        entry in the returned list will be a 1 x n matrix containing the
        constants.
        :return: Either None, a 1 x n matrix, or a list. See above for details.
        """
        echelon_matrix = self.gaussian_elimination(True)

        col = -1
        row = -1

        # checks if the matrix has a row with the leading entry in the last
        # column. If so, returns None.
        while row >= -echelon_matrix.rows and not echelon_matrix.matrix[row][col]:
            row -= 1
        if not echelon_matrix.matrix[row][col - 1]:
            return None

        row = 0
        col = 0
        
        while row < echelon_matrix.rows and col < echelon_matrix.cols:
            TODO = True

    def store_value(self, value, row: int, col: int):
        """
        Stores a value of type int or Fraction into position row x col of the
        matrix.
        :param value: The value to be stored.
        :param row: The row it is to be stored in.
        :param col: The column it is to be stored in.
        """

        # Ensures that all parameters are of appropriate types.
        if not isinstance(value, int) and not isinstance(value, Fraction) \
                or not isinstance(row, int) or not isinstance(col, int):
            raise TypeError

        # Ensures that value is of a valid type.
        if isinstance(value, int):
            value = Fraction(value, 1)

        self.matrix[row - 1][col - 1] = value

    def input_matrix(self):
        """
        Allows user to input elements into the Matrix.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                print("Value to be input in position ("
                      + str(i + 1) + ", " + str(j + 1) + ")")
                self.matrix[i][j] = Fraction.input_fraction()




test = Matrix(3, 4)

test.matrix[0][0] = Fraction(1, 1)
test.matrix[0][1] = Fraction(2, 1)
test.matrix[0][2] = Fraction(1, 1)
test.matrix[0][3] = Fraction(1, 1)

test.matrix[1][0] = Fraction(2, 1)
test.matrix[1][1] = Fraction(3, 1)
test.matrix[1][2] = Fraction(2, 1)
test.matrix[1][3] = Fraction(0, 1)

test.matrix[2][0] = Fraction(1, 1)
test.matrix[2][1] = Fraction(1, 1)
test.matrix[2][2] = Fraction(1, 1)
test.matrix[2][3] = Fraction(2, 1)

print(test.gaussian_elimination(True))
print(test)
