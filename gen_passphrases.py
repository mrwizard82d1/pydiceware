#! /cygdrive/c/Python25/python.exe


"""Module for generating passphrases (of various kinds) using
electronic diceware."""


from optparse import OptionParser

import diceware


BASIC=0
NT_LOGIN=1
XP_LOGIN=2


def gen_passphrases(style, count):
    """gen_passphrase(style, count) -> [count diceware words]

    Generates a passphrase consisting of count diceware words using
    the specified style.

    The style must be one of
    - BASIC: generate passphrases consisting of 5 diceware words.
    - NT_LOGIN: generate passphrasses consisting of 14-character
      diceware words concatenated with special characters. 
    - XP_LOGIN: generate passphrases consisting of 4 diceware words
      one of which has a character replaced with a randomly selected
      special character. 
    """

    assert count > 0, "Must generate at least one passphrase."
    assert ((style == BASIC) or (style == NT_LOGIN) or
            (style == XP_LOGIN)), \
            ("Unrecognized style %d." % style)
    
    if style == BASIC:
        generator = diceware.makeBasicGenerator()
    elif style == NT_LOGIN:
        generator = diceware.makeLoginGenerator()
    elif style == XP_LOGIN:
        generator = diceware.SpecialGenerator(count=4)

    result = [generator.next() for i in range(count)]
    return result


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-b", "--basic", action="store_const",
                      const=BASIC, dest="style",
                      help=("(Default) Generate basic diceware" +
                            " passphrases consisting of 5 random but" +
                            " easily remembered words."))
    parser.add_option("-n", "--nt", action="store_const",
                      const=NT_LOGIN, dest="style",
                      help=("Generate 14-character diceware" +
                            " passphrases consisting of diceware" +
                            " words concatenated by randomly" +
                            " selected special characters."))
    parser.add_option("-x", "--xp", action="store_const",
                      const=XP_LOGIN, dest="style",
                      help=("Generate diceware passphrases" +
                            " consisting of 4 diceware words with" +
                            " a randomly selected special character" +
                            " replacing a random character of a" +
                            " random word."))
    parser.add_option("-c", "--count",
                      help="Number of passphrases to generate" +
                      " (default=5).")
    parser.set_defaults(style=BASIC)
    parser.set_defaults(count='5')

    (options, args) = parser.parse_args()
    passphrases = gen_passphrases(options.style, int(options.count))
    for passphrase in passphrases:
        print passphrase
        
