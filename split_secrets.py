#! /cygdrive/c/Python25/python.exe


"""split_secret --count[=2]

Application (filter) for splitting secrets into count shares.
"""


from optparse import OptionParser
import sys

import diceware


def split_secret(secret, count):
    """split_secret(secret, count) -> list of shares

    Splits secret into count shares returning the list of shares.
    """
    result = diceware.splitSecret(secret, count)
    return result


if __name__ == '__main__':
    
    usage = """usage: %prog [options] [filename]

    Split a set of secrets into shares.

    The secrets consist of passphrases supplied one per line.

    If filename is supplied, the secrets are read from the file;
    otherwise, they are read from standard input.

    The program writes all the shares on a single line for each secret
    on the program's standard output.
    """
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--count', default=2,
                      help=('The number of shares into which to split' +
                            ' the secret(s) (default=2).'))

    (options, args) = parser.parse_args()
    assert ((len(args) == 0) or (len(args) == 1)), \
           ('At most one filename allowed: %d supplied.' % len(args))

    inStream = file(args[0]) if len(args) == 1 else sys.stdin
    secrets = inStream.readlines()
    for secret in secrets:
        shares = split_secret(secret, int(options.count))
        for share in shares:
            print share,
        print
        
