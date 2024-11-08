#
#   SmartReferenceControl.py
#
#   A Wx control for typing or selecting a Scripture Book+Chapter reference.
#
#

import wx
import re

import BBooks

#-----------------------------------------------------------
# RE for valid "Book Chapter" strings
referenceRE = re.compile(r"(\d |)\w(\w| )* \d+")

#-----------------------------------------------------------

myEVT_REFERENCE_UPDATED = wx.NewEventType()
EVT_REFERENCE_UPDATED   = wx.PyEventBinder(myEVT_REFERENCE_UPDATED, 1)

class ReferenceEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.Reference = None

    def SetReference(self, ref):
        self.Reference = ref

#-----------------------------------------------------------
# This class is used to provide an interface between a ComboCtrl and a
# ListCtrl that is used as the popoup for the combo widget. 
# The ListCtrl is created in Create() and returned from the GetControl
# method.

class ListCtrlComboPopup(wx.ComboPopup):
        
    def __init__(self):
        wx.ComboPopup.__init__(self)
        self.lc = None
            
    def AddItem(self, txt):
        self.lc.InsertItem(self.lc.GetItemCount(), txt)

    def OnMotion(self, evt):
        item, flags = self.lc.HitTest(evt.GetPosition())
        if item >= 0:
            self.lc.Select(item)
            self.curitem = item

    def OnLeftDown(self, evt):
        self.book = self.curitem
        self.Dismiss()

    # This is called immediately after construction finishes. You can
    # use self.GetCombo if needed to get to the ComboCtrl instance.
    def Init(self):
        self.book = -1
        self.curitem = -1

    # Create the popup child control. Return true for success.
    def Create(self, parent):
        self.lc = wx.ListCtrl(parent,
                           style=wx.LC_LIST|wx.LC_SINGLE_SEL|wx.SIMPLE_BORDER)
        self.lc.Bind(wx.EVT_MOTION, self.OnMotion)
        self.lc.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        
        return True

    # Return the widget that is to be used for the popup
    def GetControl(self):
        return self.lc

    # Called just prior to displaying the popup, you can use it to
    # 'select' the current item.
    def SetStringValue(self, val):
        if not val: return
        # Normalise the book name for lookup in the list
        if val[-1].isdigit():
            val = " ".join(val.split()[:-1])
        idx = self.lc.FindItem(-1, val.strip())
        if idx != wx.NOT_FOUND:
            self.lc.Select(idx)

    # Return a string representation of the current item.
    def GetStringValue(self):
        if self.book >= 0:
            # Appends chapter "1"
            return " ".join((self.lc.GetItemText(self.book),
                              str(1)))
        return ""

    def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        return wx.ComboPopup.GetAdjustedSize(self, minWidth,
                                             prefHeight, maxHeight)


#----------------------------------------------------------------------

class SmartReferenceControl(wx.ComboCtrl):

    def __init__(self, parent, ref=(0,0), size=wx.DefaultSize):
        wx.ComboCtrl.__init__(self, parent, size=size,
                              style = wx.TE_PROCESS_ENTER )
        self.SetButtonPosition(side=wx.LEFT)

        self.Bind(wx.EVT_TEXT, self.OnEdited)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnterKey)

        self.popup = ListCtrlComboPopup()
        self.SetPopupControl(self.popup)
        for bk in BBooks.Books():
            self.popup.AddItem(bk)

        self.Book = ref[0]
        self.Chapter = ref[1]
        self.__refreshing = False
        self.__RefreshValue()

    def __SendReference(self):
        #print "Sending Reference Event:", (self.Book, self.Chapter)
        evt = ReferenceEvent(myEVT_REFERENCE_UPDATED, self.GetId())
        evt.SetReference((self.Book, self.Chapter))
        self.GetEventHandler().ProcessEvent(evt)

    def __RefreshValue(self):
        print("__RefreshValue", self.Book, self.Chapter)
        if self.Book == 0:
            newValue = ""
        elif self.Chapter == 0:
            newValue = BBooks.Book(self.Book)+" "
        else:
            newValue = " ".join((BBooks.Book(self.Book),
                                 str(self.Chapter)))
        if newValue != self.GetValue():
            self.__refreshing = True
            self.SetValue(newValue)         # Invokes OnEdited()
            self.__refreshing = False
            self.SetInsertionPointEnd()

    def OnEdited(self, event):
        if self.__refreshing: return

        text = self.GetValue()
        print (f"OnEdited [{text}]")
        if not text:
            self.Book = 0
            self.Chapter = 0
            return

        if m := referenceRE.match(text):         # Match from beginning of the string
            text = m.group(0)        # Truncate to the valid text in case of extra chrs (e.g. ':')
            self.Book = BBooks.Lookup(text)
            if self.Book:
                self.Chapter = int(text.split()[-1])
                # Make sure that Book & Chapter are consistent.
                if self.Chapter < 1:
                    self.Chapter = 1
                if self.Chapter > BBooks.Chapters(self.Book):
                    self.Chapter = BBooks.Chapters(self.Book)
            else:
                # Invalid book name, reset
                self.Book = 0
                self.Chapter = 0
        else:
            # The user is typing a name
            self.Chapter = 0
            idx = BBooks.Lookup(text)
            if idx:
                fullName = BBooks.Book(idx)
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
                if BBooks.ValidPrefix(text):
                    # Still ambiguous, so keep the user's edits by not refreshing.
                    return
                else:
                    # Igore (i.e. delete) the last character entered since
                    # it doesn't match anything.
                    
                    self.__refreshing = True
                    self.SetValue(text[:-1])
                    self.__refreshing = False
                    self.SetInsertionPointEnd()
                    return

        self.__RefreshValue()

    def SetReferenceHandler(self, handler):
        self.Bind(EVT_REFERENCE_UPDATED, handler)
    def OnEnterKey(self, event):
        fix = False
        if self.Book == 0:
            self.Book = 1
            fix = True
        if self.Chapter == 0:
            self.Chapter = 1
            fix = True
        if fix:
            # Show the corrected value
            self.__RefreshValue()
        self.__SendReference()

    def NextChapter(self):
        if self.Book > 0:
            if self.Chapter < BBooks.Chapters(self.Book):
                self.Chapter += 1
                self.__RefreshValue()
                self.__SendReference()

    def PreviousChapter(self):
        if self.Book > 0:
            if self.Chapter > 1:
                self.Chapter -= 1
                self.__RefreshValue()
                self.__SendReference()

