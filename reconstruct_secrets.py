#! /cygdrive/c/Python25/python.exe


"""reconstruct_secrets share...

Application (filter) for reconstructing secrets from shares.
"""


from optparse import OptionParser
import sys

import diceware


def reconstruct_secret(shares):
    """reconstruct_secrets(shares) -> secret

    Reconstruct a secret from its shares.
    """
    result = diceware.restoreSecret(shares)
    return result


if __name__ == '__main__':
    
    usage = """usage: %prog [options] [filename]

    Restore a set of secrets from their shares.

    The shares consist of two or more words. A set of words on a
    single line constitute the shares for a single secret.

    If filename is supplied, the secrets are read from the file;
    otherwise, they are read from standard input.

    The program writes the secrets one per line on the program's
    standard output.
    """
    parser = OptionParser(usage=usage)

    (options, args) = parser.parse_args()
    assert ((len(args) == 0) or (len(args) == 1)), \
           ('At most one filename allowed: %d supplied.' % len(args))

    inStream = file(args[0]) if len(args) == 1 else sys.stdin
    secretsShares = inStream.readlines()
    for secretShares in secretsShares:
        shares = secretShares.split()
        secret = reconstruct_secret(shares)
        print secret
        
            

                            
                      
