Fractions are defined by a numerator and a denominator, both of which are ints. Fractions of this class are always reduced, as every method in the class reduces itself at the end. 

Fractions are represented as a string as "A/B", with A being the numerator and B being the denominator.

The boolean representation of is True if the numerator is nonzero, False if it is zero.

The +, -, *, /, \**, >, <, ==, >=, <=, and != operators have all been overloaded to work with Fractions. All return a Fraction when one or both operands are Fractions.

**Methods:**

Fraction(numerator, denominator)<br/>
    Initialize a Fraction. Arguments are the numerator and denominator, both ints.<br/>
    :param numerator: The numerator.<br/>
    :param denominator: The denominator.<br/>
  
evaluate()
    Evaluates the Fraction. Returns the int value of the Fraction if it
    exists, or the float value if not.
    :return: the int or Float value of the Fraction.

input_fraction()
    Allows the user to input a Fraction in the form "\<sign>\<numerator> /
    \<denominator>". Whitespace between elements is ignored.
    :return: The Fraction the user input.
