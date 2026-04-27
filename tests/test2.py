from openpyxl import Workbook
from pathlib import Path
from openpyxl import load_workbook
savepath = Path.home() / "Desktop/abc.xlsx"

wb = load_workbook(savepath)
ws = wb.active

ws['a1'] = '123'
ws['b2'] = 'kkkk'
ws.append()
wb.save(savepath)


