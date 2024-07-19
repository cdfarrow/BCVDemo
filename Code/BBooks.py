#
#   Static information on Biblical-books, including unique abbreviations.
#
#   

#
#    Book Name, Number of chapters, Abbreviation(s)
#

book_data = [
    None,
    ("Genesis", 50, ('Ge',)),
    ("Exodus", 40, ('Ex',)),
    ("Leviticus", 27, ('Le',)),
    ("Numbers", 36, ('Nu',)),
    ("Deuteronomy", 34, ('De', 'Dt')),
    ("Joshua", 24, ('Jos',)),
    ("Judges", 21, ('Judg', 'Jdg')),
    ("Ruth", 4, ('Ru',)),
    ("1 Samuel", 31, ('1 S', '1S')),
    ("2 Samuel", 24, ('2 S', '2S')),
    ("1 Kings", 22, ('1 K', '1K')),
    ("2 Kings", 25, ('2 K', '2K')),
    ("1 Chronicles", 29, ('1 Ch', '1Ch')),
    ("2 Chronicles", 36, ('2 Ch', '2Ch')),
    ("Ezra", 10, ('Ezr',)),
    ("Nehemiah", 13, ('Ne',)),
    ("Esther", 10, ('Es',)),
    ("Job", 42, ('Job',)),
    ("Psalms", 150, ('Ps',)),
    ("Proverbs", 31, ('Pr',)),
    ("Ecclesiastes", 12, ('Ec',)),
    ("Song of Songs", 8, ('S',)),
    ("Isaiah", 66, ('Is',)),
    ("Jeremiah", 52, ('Je',)),
    ("Lamentations", 5, ('La',)),
    ("Ezekiel", 48, ('Eze',)),
    ("Daniel", 12, ('Da',)),
    ("Hosea", 14, ('Ho',)),
    ("Joel", 3, ('Joe',)),
    ("Amos", 9, ('Am',)),
    ("Obadiah", 1, ('O',)),
    ("Jonah", 4, ('Jon',)),
    ("Micah", 7, ('Mi',)),
    ("Nahum", 3, ('Na',)),
    ("Habakkuk", 3, ('Hab',)),
    ("Zephaniah", 3, ('Zep',)),
    ("Haggai", 2, ('Hag',)),
    ("Zechariah", 14, ('Zec',)),
    ("Malachi", 3, ('Mal',)),
    None,
    ("Matthew", 28, ('Mat', 'Mt')),
    ("Mark", 16, ('Mar', 'Mk')),
    ("Luke", 24, ('Lu', 'Lk')),
    ("John", 21, ('Joh', 'Jn')),
    ("Acts", 28, ('Ac',)),
    ("Romans", 16, ('Ro',)),
    ("1 Corinthians", 16, ('1 Co', '1Co')),
    ("2 Corinthians", 13, ('2 Co', '2Co')),
    ("Galatians", 6, ('Ga',)),
    ("Ephesians", 6, ('Ep',)),
    ("Philippians", 4, ('Phili', 'Php', 'Pp')),
    ("Colossians", 4, ('C',)),
    ("1 Thessalonians", 5, ('1 Th', '1Th')),
    ("2 Thessalonians", 3, ('2 Th', '2Th')),
    ("1 Timothy", 6, ('1 Ti', '1Ti')),
    ("2 Timothy", 4, ('2 Ti', '2Ti')),
    ("Titus", 3, ('T',)),
    ("Philemon", 1, ('Phile', 'Phm', 'Pm')),
    ("Hebrews", 13, ('He',)),
    ("James", 5, ('Ja',)),
    ("1 Peter", 5, ('1 P', '1P')),
    ("2 Peter", 3, ('2 P', '2P')),
    ("1 John", 5, ('1 J', '1J')),
    ("2 John", 1, ('2 J', '2J')),
    ("3 John", 1, ('3',)),
    ("Jude", 1, ('Jude',)),
    ("Revelation", 22, ('Re',)),
    ]

abbrev_lookup = dict()
for idx, data in enumerate(book_data):
    if data:
        for abbrev in data[2]:
            if abbrev in abbrev_lookup:
                print("Error: duplicate abbreviation [%s]" % abbrev)
            abbrev_lookup[abbrev] = idx


def Book(idx):
    if idx > 0 and idx != 40:
        return book_data[idx][0]
    else:
        raise IndexError
    
def Books():
    return [bk[0] for bk in book_data if bk]

def Chapters(idx):
    if idx > 0 and idx != 40:
        return book_data[idx][1]
    else:
        raise IndexError

def Lookup(bookname):
    bookname = bookname.title()         # Title capitalization
    # First see if we have the full book name
    try:
        idx = Books().index(bookname)+1
        return idx if idx < 40 else idx+1
    except ValueError:
        pass
    # Search from longest to shortest match
    for i in range(len(bookname)):
        try:
            return abbrev_lookup[bookname[:i+1]]
        except KeyError:
            continue
    # No matches
    return 0

def ValidPrefix(prefix):
    prefix = prefix.title()
    for abbrev in abbrev_lookup:
        if len(prefix) <= len(abbrev):
            if abbrev.startswith(prefix):
                return True
    return False