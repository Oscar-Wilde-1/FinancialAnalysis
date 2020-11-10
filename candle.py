import xlrd
import datetime
import mplfinance as mpf
import pandas as pd


# author 刘钰
class Candle:
    # 判断形态
    def judge(self):
        # 打开文件，获取excel文件的workbook（工作簿）对象
        workbook = xlrd.open_workbook("D:/aaa/testData.xlsx")

        names = workbook.sheet_names()
        sheet0_name = names[0]  # 获取sheet名称
        worksheet = workbook.sheet_by_name(sheet0_name)  # 获取sheet对象

        year = int(input("输入年: "))
        month = int(input("输入月: "))
        day = int(input("输入日: "))  # 输入需要判断的日期

        delta = (datetime.date(year, month, day) - datetime.date(1900, 1, 1)).days + 2
        row = -1

        for row in range(1, worksheet.nrows):  # 在文件中寻找输入的日期
            if int(worksheet.cell_value(row, 0)) == delta:
                print("定位至" + str(year) + '/' + str(month) + '/' + str(day))
                break
            elif int(worksheet.cell_value(row, 0)) > delta and row == 1:
                print("时间输入错误，太早了！！！！")
                return
            elif int(worksheet.cell_value(row, 0)) > delta:
                row = row - 1
                date = datetime.date(1900, 1, 1) + datetime.timedelta(int(worksheet.cell_value(row, 0)) - 2)
                print("您输入的日期没有数据，已为您定位至" + str(date.year) + '/' + str(date.month) + '/' + str(date.day))
                break
        if row == 1:
            print("定位到第一天数据，无法判断形态")
            return
        if row == worksheet.nrows - 1 and int(worksheet.cell_value(row, 0)) != delta:  # 没找到就定位到最新日期
            date = datetime.date(1900, 1, 1) + datetime.timedelta(int(worksheet.cell_value(row, 0)) - 2)
            print("您输入的日期没有数据，已为您定位至" + str(date.year) + '/' + str(date.month) + '/' + str(date.day))

        # 判断形态
        form = 0
        if float(worksheet.cell_value(row - 1, 4)) > float(worksheet.cell_value(row - 1, 1)) and float(
                worksheet.cell_value(row, 1)) > float(worksheet.cell_value(row - 1, 2)) and float(
            worksheet.cell_value(row, 4)) < (
                float(worksheet.cell_value(row - 1, 1)) + float(worksheet.cell_value(row - 1, 4))) / 2:
            print("乌云盖顶")
            form = 1

        if float(
                worksheet.cell_value(row, 4)) > float(worksheet.cell_value(row - 1, 1)) > float(
            worksheet.cell_value(row - 1, 4)) > float(
            worksheet.cell_value(row, 1)):
            print("看涨吞没")
            form = 1

        if float(
                worksheet.cell_value(row, 4)) < float(worksheet.cell_value(row - 1, 1)) < float(
            worksheet.cell_value(row - 1, 4)) < float(
            worksheet.cell_value(row, 1)):
            print("看跌吞没")
            form = 1

        if form == 0:
            print("无形态")

    # 绘制k线图
    def pic(self):
        df = pd.DataFrame(pd.read_excel("D:/aaa/testData.xlsx", index_col=0))

        mpf.plot(
            data=df,
            type="candle",
            title="",
            ylabel="",
            style="binance",
            mav=(2, 5, 10),
            volume=False,
            savefig="D:/aaa/mplfinance.png"
        )
