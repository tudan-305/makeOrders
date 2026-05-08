from openpyxl import load_workbook
from openpyxl.styles import Border, Side
from openpyxl.worksheet.cell_range import CellRange
wb = load_workbook("gii.xlsx")
ws = wb.active

myRange = CellRange("a22:c34")
myBorder = Border(
    left=Side(style="thick", color="000000"),
    right=Side(style="thick", color="000000"),
    top=Side(style="thick", color="000000"),
    bottom=Side(style="thick", color="000000")
)
print(myRange.bounds)
wb.save("kk.xlsx")