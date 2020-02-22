
Fraction:

Fractions are defined by a numerator and a denominator, both of which are ints. 
Fractions of this class are always reduced, as every method in the class reduces
itself at the end. 

Fractions are represented as a string as "A/B", with A being the numerator and B 
being the denominator.

The boolean representation of is True if the numerator is nonzero, False if it is 
zero.

The +, -, *, /, \**, >, <, ==, >=, <=, and != operators have all been overloaded to 
work with Fractions.

Fraction(numerator: int, denominator: int)
    Initialize a Fraction. Arguments are the numerator and denominator.
    :param numerator: The numerator.
    :param denominator: The denominator.
  
