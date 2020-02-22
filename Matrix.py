from __future__ import annotations
from MatrixMath import Fraction


class Matrix:
    def __init__(self, rows, cols):
        """
        Creates a Matrix of dimensions rows x cols with all entries initialized
        to 0.
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

        # The following values default to None, but are calculated as a result
        # of certain methods in the class. These can be accessed safely by
        # the retrieve_{value} methods (e.g. retrieve_determinant(), etc).

                                        # TODO: Make these private and only allow the function to access them if the appropriate functions have been called.

        # Calculated by the find_determinant() method. If it exists, it is
        # stored as a Fraction.
        self.determinant_found = False
        self.determinant = None

        # Calculated by the find_inverse() method. Once found, it is stored as
        # a Matrix.
        self.inverse_found = False
        self.inverse = None

        # Calculated by the gaussian_elimination() method unless
        # stop_early_no_solution is True and the Matrix has no solution. If it
        # is found, it is stored as a Matrix.
        self.reduced_echelon_form_found = False
        self.reduced_echelon_form = None

        # Calculated by the find_solution() method. If a solution exists, it
        # will be stored as a list (see documentation for find_solution for
        # more details). If no solution exists, remains None.
        self.solution_found = False
        self.solution = None

    def retrieve_determinant(self):
        """
        Returns the determinant of self if it has been found. If if has not
        been found, returns False.
        :return: False if the determinant has not been found yet, None if there
        is no determinant, or the determinant as an int if it has been found.
        """
        if not self.determinant_found:
            return False

        return self.determinant

    def retrieve_inverse(self):
        """
        Returns the inverse of self if it has been found. If if has not been
        found, returns False.
        :return: False if the inverse has not been found yet, None if there is
        no inverse, or the inverse as a Matrix if it has been found.
        """
        if not self.inverse_found:
            return False

        return self.inverse

    def retrieve_reduced_echelon_form_found(self):
        """
        Returns the reduced echelon form matrix of self if it has been found.
        If if has not been found, returns False.
        :return: False if the reduced echelon form has not been found yet, or
        the reduced echelon form as a Matrix if it has been found.
        """
        if not self.reduced_echelon_form_found:
            return False

        return self.reduced_echelon_form

    def retrieve_solution(self):
        """
        Returns the solution of self if it has been found. If if has not been
        found, returns False.
        :return: False if the solution has not been found yet, None if there is
        no solution, or the solution as a list if it has been found. See the
        documentation for the find_solution() method for details on the
        formatting of the list.
        """
        if not self.solution_found:
            return False

        return self.solution

    def __str__(self):
        """
        Defines the string representation of a Matrix.
        :return: The string representation of self.
        """

        string = '['
        for i in range(self.rows):
            for j in range(self.cols):
                string += '{:^10}'.format(str(self.matrix[i][j]))
            if i == self.rows - 1:
                string += ']'
            string += '\n\n '
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

    def find_determinant(self, factor: Fraction):                               # TODO: Make this more intuitive for the user to use.
        """
        Returns the determinant of the matrix from which self, an echelon form
        Matrix, was computed. Determinant is only defined for a n x n Matrix.
        :return: The calculated determinant as a Fraction, or None if no
        determinant exists.
        """

        # The determinant is only defined for n x n matrices.
        if self.rows != self.cols:
            return None

        # The determinant of a 2 x 2 matrix is ad - bc (a, b, c, d from left
        # to right, top to bottom.

        if self.rows == 2:
            return self.matrix[0][0] * self.matrix[1][1] \
                   - self.matrix[0][1] * self.matrix[1][0]

        # Computes the determinant by summing the diagonal of the reduced
        # echelon form matrix and multiplying it by factor.
        determinant = Fraction(1, 1)
        for i in range(self.rows):
            determinant *= self.matrix[i][i]
        determinant *= factor

        return determinant

    def gaussian_elimination(self, stop_early_no_solution: bool = False,
                             stop_early_determinant: bool = False):
        """
        Returns either the row echelon form or the reduced row echelon form
        resulting from Gauss-Jordan elimination on self. If stop_early is True,
        the function will return the row echelon form if the leading entry in
        any row is in the last column (indicating no solutions to a linear
        system.) In all other cases, it will return the reduced row echelon
        form matrix. If the reduced row echelon form matrix is computed, will
        also find the determinant.
        :param stop_early_no_solution: Whether or not the algorithm stops after
        determining the row echelon form if there is no solution. Optional
        parameter, defaults to False.
        :param stop_early_determinant: Whether or not the algorith stops after
        determining the row echelon form regardless of whether or not there is
        a solution. Used when calculating determinants.
        :return: The resulting Matrix, or None if stop_early_determinant is
        True.
        """

        result = self.copy_matrix()
        col = 0
        row = 0

        # This is used to compute the determinant at the end of the function.
        # Multiplied by -1 when two rows are swapped and divided by the factor
        # when a row is added to another. Unchanged when a row is multiplied by
        # a scalar factor.
        det_factor = Fraction(1, 1)

        while col < result.cols and row < result.rows:
            # Finds the first row in the current column with a leading entry.
            row_search = row
            while row_search < result.rows \
                    and not result.matrix[row_search][col]:
                row_search += 1

            # Swaps the first row with the first row containing a leading
            # entry to create a pivot.
            if row_search != row and row_search != result.rows:
                det_factor *= -1
                result = result.swap_rows(row + 1, row_search + 1)

            # If there is now a leading entry, sets it to 1 to serve as the
            # pivot by dividing the entire row by the leading entry.
            if result.matrix[row][col]:
                det_factor /= 1 / result.matrix[row][col]
                result = result.multiply_row(row + 1, 1 /
                                             result.matrix[row][col])

            # Eliminates all leading entries below the pivot by subtracting the
            # appropriate amount of the leading entry's row.
            for i in range(row + 1, result.rows):
                if result.matrix[i][col]:
                    result = result.add_row(i + 1, -result.matrix[i][col],
                                            row + 1)

            col += 1

            # If a pivot was found in the column, increases row.
            if row_search != result.rows:
                row += 1

        # When calculating the determinant, there is no point in continuing
        # Gaussian elimination once an echelon form matrix has been computed.
        if stop_early_determinant:
            self.determinant = result.find_determinant(det_factor)
            self.determinant_found = True
            return None

        # If stop_early_no_solution is True, checks if the Matrix has no
        # solution. If so, returns the Matrix early without computing the
        # reduced echelon form.
        if stop_early_no_solution:
            col = -1
            row = -1

            # Searches for the last row to contain an entry in the last column.
            while row >= -result.rows and not result.matrix[row][col]:
                row -= 1

            # Checks if the entry in that row is a leading entry.
            is_leading = True
            while col >= -result.cols + 1:
                if result.matrix[row][col - 1]:
                    is_leading = False
                col -= 1
            if is_leading:
                return result

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

        # Computes the determinant and stores in self.determinant.
        self.reduced_echelon_form_found = True
        self.reduced_echelon_form = result
        return result

    def find_solution(self):
        """
        Finds the solution for the system of linear equations defined by the
        Matrix self. Solution is None if no solution, an n x 1 matrix for just
        one solution with n being the number of variables, and a list if there
        are infinite solutions. The list consists of m lists containing the
        numbers of the independent variables and the vectors associated with
        them, written as lists of length m, where m is the number of variables.
        The last entry in the returned list will be another list of length m
        containing the constants. The computed solution is stored in
        self.solution.
        :return: None
        """
        echelon_matrix = self.gaussian_elimination(True)

        col = -1
        row = -1

        # checks if the matrix has a row with the leading entry in the last
        # column. If so, stores None into self.solution and returns None to
        # end the function call.
        while row >= -echelon_matrix.rows \
                and not echelon_matrix.matrix[row][col]:
            row -= 1
        if not echelon_matrix.matrix[row][col - 1]:
            self.solution = None
            return None

        row = 0
        col = 0
        independent = []

        # Searches for columns in the reduced echelon form matrix representing
        # independent variables and stores the number of the column in a list.
        while col < echelon_matrix.cols - 1:
            if row != echelon_matrix.rows and echelon_matrix.matrix[row][col]:
                row += 1
            else:
                independent.append(col)
            col += 1

        # Creates the list that will be returned. The last element will be a
        # list containing the constants.
        solution = []
        for i in independent:
            independent_vector = []
            for j in range(echelon_matrix.rows):
                if j == i:
                    independent_vector.append(1)
                else:
                    independent_vector.append(-echelon_matrix.matrix[j][i])
            solution.append([i, independent_vector])

        # Adds a final list to the solution containing the constants.
        constant_vector = []
        for i in range(echelon_matrix.rows):
            constant_vector.append(echelon_matrix.matrix[i][col])
        solution.append(constant_vector)

        self.solution_found = True
        self.solution = solution

    def output_solution(self):                                              #TODO: Allow it to deal with solutions containing only one line.
        """
        Takes a solution obtained by find_solution() and returns it as a
        formatted string. If no solution exists, returns None
        :param solution: The solution. For more details on the format, see the
        documentation for find_solution().
        :return: The solution formatted as a string or None.
        """

        solution = self.retrieve_solution()

        # Deals with the possibility of no solution.
        if self.solution is None:
            return None

        # Loops through the list containing the solution and generates an
        # output string one row at a time.
        string = ''
        for i in range(len(solution[-1])):
            # Adds a variable to the start of a line. If it is the first row,
            # adds a '[' at the start to indicate the start of the Matrix and
            # an '='. If it is the last row, adds a ']' to indicate the end of
            # the Matrix.
            if i == 0:
                string += '[{:^10}  = '.format('x' + str(i + 1))
            elif i == len(solution[-1]) - 1:
                string += ' {:^10}]    '.format('x' + str(i + 1))
            else:
                string += ' {:^10}    '.format('x' + str(i + 1))

            # Adds all the independent variables and their coefficients to the
            # current row. Only prints the variable in the first row and adds a
            # '+' after the entry in the first row.
            for j in range(len(solution) - 1):
                if i == 0:
                    string += '{} [{:^10}   + '.format('x'
                                                       + str(solution[j][0] + 1),
                                                       str(solution[j][1][i]))
                elif i == len(solution[-1]) - 1:
                    string += \
                        '    {:^10}]    '.format(str(solution[j][1][i]))
                else:
                    string += \
                        '    {:^10}     '.format(str(solution[j][1][i]))

            # Adds the constant to the current row.
            if i == 0:
                string += '[{:^10} '.format(str(solution[-1][i]))
            elif i == len(solution[-1]) - 1:
                string += '{:^10}]'.format(str(solution[-1][i]))
            else:
                string += ' {:^10} '.format(str(solution[-1][i]))

            string += '\n'

        return string

    def find_inverse(self):
        """
        Returns the inverse of self. If self has no inverse, returns None.
        Also stores the inverse in self.inverse.
        :return: A Matrix that is the inverse of self if one exists, None if
        self has no inverse.
        """

        # If a Matrix is not n x n, it cannot have an inverse.
        if self.rows != self.cols:
            return None

        # Creates an n x 2n Matrix with in the left 3 columns and the identity
        # matrix in the right n columns.
        identity_appended = Matrix(self.rows, 2 * self.rows)
        for row in range(self.rows):
            for col in range(2 * self.rows):
                if col < self.rows:
                    identity_appended.matrix[row][col] = self.matrix[row][col]
                elif col - self.rows == row:
                    identity_appended.matrix[row][col] = 1
                else:
                    identity_appended.matrix[row][col] = 0

        ref = identity_appended.gaussian_elimination(False)

        # Checks if the left side of the reduced echelon form matrix is an
        # identity matrix. If not, returns None.
        for i in range(self.rows):
            if ref.matrix[i][i] != 1:
                return None

        inverse = Matrix(self.rows, self.cols)

        # Copies the right half of the reduced echelon form that was
        # originally an identity matrix and is now the inverse into a new
        # matrix.
        for i in range(inverse.rows):
            for j in range(inverse.cols):
                inverse.matrix[i][j] = ref.matrix[i][j + inverse.cols]

        return inverse

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
