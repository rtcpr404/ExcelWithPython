#นำเข้าโมดูล string, re (regular expressions), print และ Table จาก rich สำหรับการจัดการสตริง, การจัดการสูตรและการแสดงผลตาราง
import string
import re
from rich import print
from rich.table import Table

def refCal(formula, table, visited=None):#ฟังก์ชันนี้จัดการกับสูตรที่มีการอ้างอิงถึงเซลล์อื่น ๆ ในตาราง มันจะส่งคืนสูตรที่มีค่าในเซลล์แทนการอ้างอิง

    if not formula.startswith('='):
        return formula

    if visited is None:
        visited = set()

    cell_refs = re.findall(r'[A-Za-z]\d+', formula)
    for ref in cell_refs:
        col, row = cell_idx(ref)

        if col > len(table) - 1 or row > len(table[col]) - 1:
            return "#ERROR"
        cell = (col, row)

        if cell not in visited:
            visited.add(cell)
            value = evalCal(refCal(table[col][row], table, visited), table) \
                if table[col][row].startswith('=') \
                else table[col][row]

            formula = formula.replace(ref, str(value))
            visited.remove(cell)
    return formula[1:]


def evalCal(formula, table):#ฟังก์ชันนี้ใช้สำหรับการประมวลผลสูตรที่ได้จาก refCal และส่งคืนผลลัพธ์ของการคำนวณ ถ้ามีข้อผิดพลาดให้ขึ้น #ERROR

    try:
        cell_refs = re.findall(r'[A-Za-z]\d+', formula)

        for ref in cell_refs:
            col, row = cell_idx(ref)

            if col >= len(table) or row >= len(table[col]):
                return "#ERROR"

        result = eval(formula)
        return result

    except (NameError, SyntaxError, ZeroDivisionError):
        return "#ERROR"


def upCell(col_idx, row_idx, table):#ฟังก์ชันนี้ใช้สำหรับการอัปเดตเซลล์ที่มีสูตรที่อ้างอิงถึงเซลล์ที่เพิ่งถูกเปลี่ยนแปลง

    relatCell = find_cells(col_idx, row_idx, table)

    for col, row in relatCell:
        formula = table[col][row]
        pCal = refCal(table[col][row], table)
        result = evalCal(pCal, table)
        table[col][row] = result
        upCell(col, row, table)
        table[col][row] = formula


def find_cells(col_idx, row_idx, table):#ฟังก์ชันนี้ค้นหาเซลล์ที่มีสูตรที่อ้างอิงถึงเซลล์ที่กำหนด (col_idx, row_idx) และส่งคืนรายการของเซลล์

    relatCell = []

    for col in range(1, len(table)):
        for row in range(1, len(table[col])):

            if isinstance(table[col][row], str) and table[col][row].startswith('='):
                cell_refs = re.findall(r'[A-Za-z]\d+', table[col][row])

                if f"{string.ascii_uppercase[col_idx - 1]}{row_idx}" in cell_refs:
                    relatCell.append((col, row))

    return relatCell

def cell_idx(cell):#ฟังก์ชันนี้แปลงตัวอ้างอิงเซลล์เป็นคอลัมน์และแถว

    col_idx = ord(cell[0].upper()) - 64
    row_idx = int(cell[1:])

    return col_idx, row_idx

def createTable(rows, cols):#ฟังก์ชันนี้สร้างตารางเปล่าที่มีขนาดตามค่าที่รับเข้ามาจากผู้ใช้ และกำหนดค่าเริ่มต้นให้กับแถวและคอลัมน์

    table = [[' ' for j in range(rows + 1)] for i in range(ord(cols) - 64 + 1)]

    for i in range(1, rows + 1):
        table[0][i] = str(i)

    for i, c in enumerate(string.ascii_uppercase[:ord(cols) - 64]):
        table[i + 1][0] = c

    return table

def Incol(): #ฟังก์ชันนี้รับข้อมูลคอลัมน์ที่ผู้ใช้ป้อน และตรวจสอบว่าใช่อักษรภาษาอังกฤษหรือไม่ ถ้าไม่ใช่ จะแสดงข้อความข้อผิดพลาดและขอให้ป้อนใหม่

    while True:

        col = input("Input Column (A-Z): ")

        if col.upper() not in string.ascii_uppercase:
            print("invalid Column ( Try again )")

        else:
            return col.upper()

def Inrow():#ฟังก์ชันนี้รับข้อมูลแถวที่ผู้ใช้ป้อน และตรวจสอบว่าเป็นจำนวนเต็มระหว่าง 1 ถึง 100 หรือไม่ ถ้าไม่ใช่ จะแสดงข้อความข้อผิดพลาดและขอให้ป้อนใหม่

    while True:

        try:
            row = int(input("Input Row (1-100): "))

            if not (1 <= row <= 100):
                print("invalid Column ( Try again )")

            else:
                return row

        except ValueError:
            print("invalid Column ( Try again )")

def main_Table(rows, cols, table):#ฟังก์ชันนี้เป็นฟังก์ชันหลักในโปรแกรมที่ใช้สำหรับแสดงตาราง, รับข้อมูลเซลล์และข้อมูลจากผู้ใช้ และปรับปรุงตารางตามความต้องการของผู้ใช้
    while True:

        before_cal = Table()
        result_cal = Table()

        for i in range(ord(cols) - 64 + 1):
            before_cal.add_column(table[i][0]
                                       , justify="center"
                                       , no_wrap=True)

            result_cal.add_column(table[i][0]
                                      , justify="center"
                                      , no_wrap=True)

        for i in range(1, rows + 1):
            before_cal.add_row(*[str(table[j][i])
                                      for j in range(ord(cols) - 64 + 1)])

            result_cal.add_row(*[str(evalCal(refCal(table[j][i], table, set()), table))

                                     if table[j][i].startswith('=')
                                     else str(table[j][i])
                                     for j in range(ord(cols) - 64 + 1)
                                     ])


        print("Table Before Calculating:")
        print(before_cal)

        print("Table Result Calculating:")
        print(result_cal)


        cell_Inputdata = input("Input Cell And Info ( Type 'out' to close ): ")

        if cell_Inputdata == "out":
            break

        try:

            col_idx, row_idx = cell_idx(cell_Inputdata)

            if not (1 <= col_idx <= ord(cols) - 64) or not (1 <= row_idx <= rows):
                print("Invalid Cell ( Try again )")
                continue

            data = input("Input Info: ")

            if data.startswith('='):
                pCal = refCal(data, table, set())
                result = evalCal(pCal, table)
                print(f"Formula: {data} = {result}")
                table[col_idx][row_idx] = data

            else:
                table[col_idx][row_idx] = data
            upCell(col_idx, row_idx, table)

        except (ValueError, IndexError):
            print("Invalid Cell ( Try again )")

cols = Incol()
rows = Inrow()
table = createTable(rows, cols)
main_Table(rows, cols, table)