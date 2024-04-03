"""Models a single die."""


import base64
import os
import sys


class Die(object):
    """Models a single die."""

    def __init__(self):
        pass

    def roll(self):
        """Roll the die."""
        theText = os.urandom(1)
        aByte = ord(theText)
        theResult = (aByte % 6) + 1
        return theResult

    
class Dice(object):
    """Models a collection of dice."""

    def __init__(self, count):
        self._dice = [None] * count
        for i in range(count):
            self._dice[i] = Die()

    def roll(self):
        """Role the dice."""
        theResult = [theDie.roll() for theDie in self._dice]
        return theResult


class PhraseList(object):
    """Models the Diceware word list."""

    def __init__(self):
        self._words = {}
        theFile = self.findFile()
        theLines = theFile.readlines()
        theLines = theLines[2:-11]
        for theLine in theLines:
            index, phrase = theLine.split()
            self._words[int(index)] = phrase
        theFile.close()

    def findFile(self):
        """Find the diceware word list."""
        theFilename = 'diceware.wordlist.txt'
        for theSearchPath in sys.path:
            theWalker = os.walk(theSearchPath)
            for theTop, theDirnames, theFilenames in theWalker:
                if theFilename in theFilenames:
                    thePath = os.path.join(theTop, theFilename)
                    return open(thePath)

        return open(theFilename)

    def getPhrase(self, index):
        actualIndex = index
        theResult = self._words[actualIndex]
        return theResult


ourSpecChars = [ ['~', '!', '#', '$', '%', '^'],
                 ['&', '*', '(', ')', '-', '='],
                 ['+', '[', ']', '\\', '{', '}'],
                 [':', ';', '"', "'", '<', '>'],
                 ['?', '/', '0', '1', '2', '3'],
                 ['4', '5', '6', '7', '8', '9'] ]


class Generator(object):
    """Models the Diceware passphrase generator."""

    def __init__(self, count=5):
        self._count = count
        self._stream = self.stream()
        self._minSize = 14

    def buildIndex(self, theRolls):
        """Build an integer index from a set of dice rolls."""
        theResult = 0
        for theRoll in theRolls:
            theResult *= 10
            theResult += theRoll
        return theResult

    def __next__(self):
        """Generate the next passphrase."""
        theResult = next(self._stream)
        while(len(theResult) < self._minSize):
            theResult = next(self._stream)
        return theResult
    
    def stream(self):
        """Generate a stream of passphrases."""
        theDice = Dice(5)
        theList = PhraseList()
        while(True):
            thePhrases = []
            for i in range(self._count):
                theIndex = self.buildIndex(theDice.roll())
                thePhrase = theList.getPhrase(theIndex)
                thePhrases.append(thePhrase)
            theResult = ' '.join(thePhrases)
            yield theResult


class LoginGenerator(Generator):
    """Models a Diceware login generator."""

    def __init__(self, maxSize=14):
        super(LoginGenerator, self).__init__(count=(maxSize // 4) + 1)
        self._dice = Dice(2)
        self._maxSize = maxSize
        self._minSize = maxSize

    def generateSpecialChars(self, count):
        """Generate a list of special characters."""
        theResult = []
        while len(theResult) < count:
            theRoll = self._dice.roll()
            theIndices = [spots - 1 for spots in theRoll]
            theSpecialChar = ourSpecChars[theIndices[0]][theIndices[1]]
            theResult.append(theSpecialChar)
        return theResult
    
    def __next__(self):
        """Calculate the next password."""
        while True:
            theRawList = super(LoginGenerator, self).__next__().split()
            theSpecialChars = self.generateSpecialChars(len(theRawList) - 1)
            thePhraseList = [theRawList[0]]
            for i in range(len(theSpecialChars)):
                thePhraseList.append(theSpecialChars[i])
                thePhraseList.append(theRawList[i + 1])
            thePhrase = ''.join(thePhraseList)
            if len(thePhrase) >= self._maxSize:
                theResult = thePhrase[:self._maxSize]
                break
        return theResult


class SpecialGenerator(Generator):
    """Models a Diceware passphrase generator.

    This instance includes a special character in the passphrase for
    an additional 10 bits of entropy.
    """ 

    def __init__(self, count=5):
        super(SpecialGenerator, self).__init__(count)
        self._dice = Dice(4)

    def insertSpecial(self, theRawPassphrase):
        """Insert a special character at a random location."""
        thePhrases = theRawPassphrase.split()
        while True:
            theRoll = self._dice.roll()
            theIndices = [spots - 1 for spots in theRoll]
            if theIndices[0] < self._count:
                wordToReplace = thePhrases[theIndices[0]]
                if theIndices[1] < len(wordToReplace):
                    theSpecChar = ourSpecChars[theIndices[2]][theIndices[3]]
                    theSpecialWord = wordToReplace[:theIndices[1]] + \
                                     theSpecChar + \
                                     wordToReplace[theIndices[1] + 1:]
                    thePhrases[theIndices[0]] = theSpecialWord
                    theResult = ' '.join(thePhrases)
                    break
        return theResult
        
    def __next__(self):
        """Calculate the next passphrase."""
        theRawPassphrase = next(super(SpecialGenerator, self))
        theResult = self.insertSpecial(theRawPassphrase)
        return theResult



def makeBasicGenerator():
    """Creates a basic, 5-word passphrase generator."""
    theResult = Generator()
    return theResult


def makeLoginGenerator(maxSize=14):
    """Create a login password generator of the specified size."""
    theResult = LoginGenerator(maxSize)
    return theResult


def makeSpecialGenerator():
    """Creates a basic generator with a replacement special character."""
    theResult = SpecialGenerator()
    return theResult


def splitSecret(passPhrase, sharesCount=2):
    """Splits a passPhrase into two shares."""
    thePool = RandomPool()
    randomBits = [None] * (sharesCount - 1)
    for i in range(sharesCount - 1):
        thePool.stir()
        randomBits[i] = thePool.get_bytes(len(passPhrase))

    lastShareList = [ord(p) for p in passPhrase]
    for i in range(len(randomBits)):
         for j in range(len(passPhrase)):
             lastShareList[j] ^= ord(randomBits[i][j])
    lastShare = ''.join(chr(ch) for ch in lastShareList)

    sharesList = randomBits + [lastShare]
    sharesListText = [base64.b64encode(s) for s in sharesList]
    theResult = tuple(sharesListText)
    return theResult


def restoreSecret(shares):
    """Reconstitutes a secret split into two shares."""
    sharesLists = [[ord(ch) for ch in list(base64.b64decode(sl))] for
                   sl in list(shares)]
    theSecretList = [''] * len(sharesLists[0])
    for i in range(len(sharesLists[0])):
        theSecretList[i] = sharesLists[0][i]
        for j in range(1, len(sharesLists)):
            theSecretList[i] ^= sharesLists[j][i]
    theSecret = ''.join([chr(s) for s in theSecretList])
    return theSecret
                            
    
