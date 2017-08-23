import os
import win32com.client

if os.path.exists("plan.xlsm"):
	xl=win32com.client.Dispatch("Excel.Application")
	xl.Workbooks.Open(Filename="C:\\Users\\Chutchai\\Documents\\git\\autoberth\\plan.xlsm")
	xl.Application.Run("plan.xlsm!module1.createSchedule")
	xl.AlertBeforeOverwriting = False
	xl.DisplayAlerts = False
	xl.Application.Save(True)
	xl.Application.Quit() # Comment this out if your excel script closes

	# xlApp = client.Dispatch("Excel.Application")
	xl=win32com.client.Dispatch("Excel.Application")
	xl.AlertBeforeOverwriting = False
	xl.DisplayAlerts = False
	books = xl.Workbooks.Open(Filename="C:\\Users\\Chutchai\\Documents\\git\\autoberth\\plan.xlsm")
	ws = books.Worksheets[0]
	# ws.Visible = 1
	ws.ExportAsFixedFormat(1, 'C:\\Users\\Chutchai\\Documents\\git\\autoberth\\plan.pdf')
	xl.Application.Save(True)
	xl.Application.Quit() # Comment this out if your excel script closes

	del xl
	# , ReadOnly=1