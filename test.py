import os
import win32com.client

if os.path.exists("test.xlsm"):
	xl=win32com.client.Dispatch("Excel.Application")
	xl.Workbooks.Open(Filename="C:\\Users\\Chutchai\\Documents\\git\\autoberth\\test.xlsm")
	xl.Application.Run("test.xlsm!module1.createSchedule")
	xl.AlertBeforeOverwriting = False
	xl.DisplayAlerts = False
	xl.Application.Save(True)
	xl.Application.Quit() # Comment this out if your excel script closes
	del xl
	# , ReadOnly=1