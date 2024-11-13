#
#   SmartReference.py
#
#   Logic for implementing a smart text control for typing a Scripture 
#   Book+Chapter reference. It auto-completes the book names and provides
#   custom abbreviations for efficient keyboard entry of a book and chapter.
#
#   Craig Farrow
#   2012-2024
#
import re

from . import BibleBooks

#-----------------------------------------------------------
# RE for valid "Book Chapter" strings
referenceRE = re.compile(r"(\d |)\w(\w| )* \d+")

#-----------------------------------------------------------

class SmartReference():

    def __init__(self, ref=(0,0)):
        self.Book = ref[0]
        self.Chapter = ref[1]

    def Value(self):
        if self.Book == 0:
            return ""
        elif self.Chapter == 0:
            return BibleBooks.Book(self.Book)+" "
        else:
            return " ".join((BibleBooks.Book(self.Book),
                                 str(self.Chapter)))

    def Input(self, text):
        
        print (f"SmartReference.Input[{text}]")
        if not text:
            self.Book = 0
            self.Chapter = 0
            return False

        if m := referenceRE.match(text):  # Match from beginning of the string
            text = m.group(0)             # Truncate to the valid text in case of extra chrs (e.g. ':')
            self.Book = BibleBooks.Lookup(text)
            if self.Book:
                self.Chapter = int(text.split()[-1])
                # Make sure that Book & Chapter are consistent.
                if self.Chapter < 1:
                    self.Chapter = 1
                if self.Chapter > BibleBooks.Chapters(self.Book):
                    self.Chapter = BibleBooks.Chapters(self.Book)
            else:
                # Invalid book name, reset
                self.Book = 0
                self.Chapter = 0
        else:
            # The user is typing a name
            self.Chapter = 0
            idx = BibleBooks.Lookup(text)
            if idx:
                fullName = BibleBooks.Book(idx)
                if text == fullName:
                    # Full name without space, so the user must have pressed
                    # Backspace. Clear the field.
                    self.Book = 0
                    self.Chapter = 0
                else:
                    # Auto-complete the book name
                    self.Book = idx
            else:
                # Check for a valid sequence
                if BibleBooks.ValidPrefix(text):
                    # Still ambiguous, so keep the user's edits by not refreshing.
                    return False
                else:
                    # Discard the last character entered since it doesn't 
                    # match anything.
                    
                    return text[:-1]

        return self.Value()
        
    def NextChapter(self):
        if self.Book > 0:
            if self.Chapter < BibleBooks.Chapters(self.Book):
                self.Chapter += 1
                return True
        return False
        
    def PreviousChapter(self):
        if self.Book > 0:
            if self.Chapter > 1:
                self.Chapter -= 1
                return True
        return False
        
