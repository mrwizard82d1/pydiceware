#! /cygdrive/c/Python25/python.exe


"""Implements generating random but rememberable passwords.

This module implements a program for generating passwords using an
electronic version of diceware (http://www.diceware.com) that uses a
text-oriented, interactive commander user interface.
"""


import cmd
import pprint

import diceware


def printPassphrases(generator, count):
    """o.printPassphrases(generator, count)

    Print count passphrases, each on a single line, generated by
    generator.
    """
    passphrases = [next(generator) for i in range(int(count))]
    for passphrase in passphrases:
        print(passphrase)


class CmdDiceware(cmd.Cmd):
    """Implements the interface for the diceware application."""

    def __init__(self):
        """Create a default instance."""
        cmd.Cmd.__init__(self)
        
        self._passphraseGenerator = None
        self._ntGenerator = None
        self._xpGenerator = None

    def do_EOF(self, unused):
        """Exit the application."""

        return self.do_exit(unused)
    
    def do_exit(self, unused):
        """Command: exit

        Exit the application.
        """

        return True

    def do_nt(self, count):
        """Command: nt count
        
        Generate count login passwords suitable for Windows NT.

        Windows systems limit the number of characters in login
        passwords. For example, Windows NT only uses 14 characters.

        Because of this limit, a basic diceware passphrase will not
        have the full 64.6 bits of entropy.

        To work around this issue, this function generates a basic
        (5-word) passphrase, generates 4 randomly selected special
        characters (each containing 10 bits of entropy), concatenates
        the 5-word passphrase using the special characters, and
        truncates the resulting long single word to 14 characters."""

        if not self._ntGenerator:
            self._ntGenerator = diceware.makeLoginGenerator()
        
        printPassphrases(self._ntGenerator, count)

    def do_passphrase(self, count):
        """Command: passphrase count
        
        Generate count basic (and secure) 5 word passwords.

        Because these word is from a 'dictionary' of 7776 words,
        the entropy of each word is about 12.9 bits. Consequently, a
        password consisting of 5 diceware words hase about 64.6 bits
        of entropy. Although technical, this many bits of entry means
        that an attack guessing passwords, even knowing the
        dictionary, requires about 2 ^ 64 attempts.

        More importantly, because each word averages only 4.2
        characters in length (the largest is 6 characters) , it is far
        easier for someone to memorize this difficult to guess
        password than to memorize a completely random password. 
        """
        if not self._passphraseGenerator:
            self._passphraseGenerator = diceware.makeBasicGenerator()

        printPassphrases(self._passphraseGenerator, count)

    def do_split(self, params):
        """Command: split secret [count(=2)]
        
        Splits a secret into count shares.

        To reconstruct the secret, all shares must be available.
        """
        countIndex = params.rfind(' ')
        assert countIndex > 0, \
               ("Incorrect number of parameters: expected" +
                " at least two separated by spaces.")
        secret = params[:countIndex]
        countText = params[countIndex + 1:]
        count = int(countText)
        assert count >= 2, "Number of shares, %s, must be > 2."

        shares = diceware.splitSecret(secret, count)
        for share in shares:
            print(share)

    def do_reconstruct(self, params):
        """Command: reconstruct share...
        
        Reconstruct a secret from all its shares.
        """

        shares = params.split()
        secret = diceware.restoreSecret(shares)
        print(secret)

    def do_xp(self, count):
        """Command: xp count
        
        Generate count login passwords suitable for Windows XP.

        Windows 2000 and XP systems limit the number of characters in
        login passwords to 127 characters.

        Because of this limit, a basic diceware passphrase may not
        have the full 64.6 bits of entropy.

        To work around this issue, this function generates a 4-word
        passphrase and replaces a randomly chosen character of one of
        these words with a special character."""

        if not self._xpGenerator:
            self._xpGenerator = diceware.SpecialGenerator(count=4)

        printPassphrases(self._xpGenerator, count)
    

if __name__ == '__main__':
    CmdDiceware().cmdloop()
    
