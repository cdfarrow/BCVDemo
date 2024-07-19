Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "Code"
WshShell.Run "py BCVDemo.py", 0
WshShell = Null
