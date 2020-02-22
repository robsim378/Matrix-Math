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
        "A/B", A being the numerator and B being the denominator
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
            numerator_input = 0
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
                numerator_input *= 10
                numerator_input += int(value[i])
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

                while i != len(value) and value[i] == ' ':
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

        return Fraction(sign * numerator_input, denominator_input)

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
