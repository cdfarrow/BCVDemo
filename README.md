The SmartReferenceControl implements a Biblical reference selector for Book and Chapter. The main features are:

+ Auto-completes the full book name once it is unambiguous. This means, in most cases, that the user just needs to type a couple of letters to get the full book name. E.g. 'pr' for Proverbs, 'ps' for Psalms, '1j' for 1 John, and the single letter 't' for Titus. Some books need a longer sequence to distinguish them, the worst case in English being 'phile' for Philemon vs 'phili' for Philippians.
+ Common book abbreviations are also supported such as 'mk' for Mark. For the two 'Ph' books above, the abbreviations 'phm' and 'php' are supported. Additionally, extra two-letter abbreviations are defined as shortcuts for books with common prefixes. E.g. 'ek' for Ezekiel vs 'er' for Ezra; 'hb' for Habakkuk and 'Hg' for Haggai (note that 'he' is already the abbreviation for Hebrews). These can be changed as desired.
+ Standard 3-letter book abbreviations are supported for pasting references. [Known limitation: JUD doesn't work as it conflicts with Judges and is not unambiguous.] 
+ Accepts space or no space between # and book name (e.g. '1k' or '1 k' for 1 Kings).
+ Extra letters are ignored once the book name is completed so there's no problem if the user types more than needed.
+ Extra things typed or pasted after the chapter number are ignored (so pasting a full reference such as 'mt 5:11-22' will produce 'Matthew 5').
+ Case is ignored; the reference is always formatted in title caps.
+ Auto-fixes the chapter number if it is out-of-range, so the user can enter 9 or 99 to get the last chapter in the book. E.g. 're 99' to choose 'Revelation 22'
+ Smart back-space: clears the whole bookname if Backspace is pressed when there is no chapter number, otherwise behaves normally.
+ If the user edits the string at the beginning or in the middle, then it continues to enforce valid content by either discarding the change (refreshes to what was there), or if it is a new valid prefix then it truncates the string at the cursor. If it is unambiguous at this point, then it will auto-complete.
