import datetime
import xlrd

tables = []  # 计算RSI值所需数组
DateRow = -1  # 用户输入的时间对应的数据，所在excel中的行数
DIFF = 0  # 用户输入的日期对应的当天diff值（diff = EMA(12) – EMA(26)）


# 将用户输入的时间转换为excel数据中的行数
def SwitchTime():
    year = int(input("输入年: "))
    month = int(input("输入月: "))
    day = int(input("输入日: "))  # 输入需要判断的日期

    delta = (datetime.date(year, month, day) - datetime.date(1900, 1, 1)).days + 2
    global DateRow
    for DateRow in range(1, sheet.nrows):  # 在文件中寻找输入的日期
        if int(sheet.cell_value(DateRow, 0)) == delta:
            break
        elif int(sheet.cell_value(DateRow, 0)) > delta and DateRow == 1:
            print("时间输入错误，太早了！！！！")
            return
        elif int(sheet.cell_value(DateRow, 0)) > delta:
            DateRow = DateRow - 1
            date = datetime.date(1900, 1, 1) + datetime.timedelta(int(sheet.cell_value(DateRow, 0)) - 2)
            print(str(date.year) + '/' + str(date.month) + '/' + str(date.day))
            break

    if DateRow == sheet.nrows - 1 and int(sheet.cell_value(DateRow, 0)) != delta:  # 没找到就定位到最新日期
        date = datetime.date(1900, 1, 1) + datetime.timedelta(int(sheet.cell_value(DateRow, 0)) - 2)
        print(str(date.year) + '/' + str(date.month) + '/' + str(date.day))

    # 将DateRow从数组下标转换为excel中的行数
    DateRow += 1


# 计算RSI值
def CaculateRSI():
    # day强制类型转换为int,防止用户输入奇怪的东西
    # 参数day：从用户输入日期开始，day天以内的数据被用来计算RSI值
    day = int(input("请输入X天以内数据用来计算RSI值，X= "))

    # 判断day是否合法
    if day >= sheet.nrows or (DateRow - day) < 1:
        print("时间超过数据存储范围！\n请重新输入合适时间！\n")
        return -1
    for rown in range(DateRow - day, DateRow):  # 从用户输入的日期开始，前day天内数据放入list存入tables中
        list = [sheet.cell_value(rown, 1), sheet.cell_value(rown, 2),
                sheet.cell_value(rown, 3), sheet.cell_value(rown, 4)]
        tables.append(list)
    # print(tables)

    RosePrcie = 0  # day天内，上涨收盘价总和
    FallPrice = 0  # day天内，下跌收盘价总和
    RoseDay = 0  # day天内，上涨的天数
    FallDay = 0  # day天内，下跌的天数
    for element in tables:  # 遍历table中所有元素
        if element[0] > element[3]:  # 如果收盘价低于开盘价，则该天算做下跌
            FallPrice += element[3]
            FallDay += 1
        else:  # 如果收盘价高于开盘价，则该天算做上涨
            RosePrcie += element[3]
            RoseDay += 1
    # 如果day天内未有下跌收市值(除数为0)，直接返回
    if FallDay == 0:
        print(day, "天内未有下跌收市值(除数为0)请重新输入天数！")
        return -1
    # 如果day天内未有上涨收市值(除数为0)，直接返回
    if RoseDay == 0:
        print(day, "天内未有上涨收市值(除数为0)请重新输入天数！")
        return -1
    # 计算RS值，RS = X天内上涨收市价的平均值  ÷ X天内下跌收市价的平均值
    RS = (RosePrcie / RoseDay) / (FallPrice / FallDay)
    # RSI = 100 – (100÷（1+RS）)
    RSI = 100 - (100 / (1 + RS))
    # 当RSI值大于70时，提示超买。当RSI值小于30时，提示超卖。
    if RSI > 70:
        print("RSI值为：", RSI, "超买")
    elif RSI < 30:
        print("RSI值为：", RSI, "超卖")
    else:
        print("RSI值为：", RSI)
    return RSI

# 计算RSI值
# 参数row为某一行的rsi值
def CaculateRSI(row):
    # day强制类型转换为int,防止用户输入奇怪的东西
    # 参数day：从用户输入日期开始，day天以内的数据被用来计算RSI值
    # day = int(input("请输入X天以内数据用来计算RSI值，X= "))
    day = 7 # 调试中，暂定day为7天

    # 判断day是否合法
    if day >= sheet.nrows or (row - day) < 1:
        print("时间超过数据存储范围！\n请重新输入合适时间！\n")
        return -1
    for rown in range(row - day, row):  # 从用户输入的日期开始，前day天内数据放入list存入tables中
        list = [sheet.cell_value(rown, 1), sheet.cell_value(rown, 2),
                sheet.cell_value(rown, 3), sheet.cell_value(rown, 4)]
        tables.append(list)
    # print(tables)

    RosePrcie = 0  # day天内，上涨收盘价总和
    FallPrice = 0  # day天内，下跌收盘价总和
    RoseDay = 0  # day天内，上涨的天数
    FallDay = 0  # day天内，下跌的天数
    for element in tables:  # 遍历table中所有元素
        if element[0] > element[3]:  # 如果收盘价低于开盘价，则该天算做下跌
            FallPrice += element[3]
            FallDay += 1
        else:  # 如果收盘价高于开盘价，则该天算做上涨
            RosePrcie += element[3]
            RoseDay += 1
    # 如果day天内未有下跌收市值(除数为0)，直接返回
    if FallDay == 0:
        print(day, "天内未有下跌收市值(除数为0)请重新输入天数！")
        return -1
    # 如果day天内未有上涨收市值(除数为0)，直接返回
    if RoseDay == 0:
        print(day, "天内未有上涨收市值(除数为0)请重新输入天数！")
        return -1
    # 计算RS值，RS = X天内上涨收市价的平均值  ÷ X天内下跌收市价的平均值
    RS = (RosePrcie / RoseDay) / (FallPrice / FallDay)
    # RSI = 100 – (100÷（1+RS）)
    RSI = 100 - (100 / (1 + RS))
    print(RSI)
    return RSI

# 递归函数，计算12日的EMA，计算公式：EMA（12）=前一日的EMA(12)×11÷13+今日收盘价×2÷13
# 参数row为当前日期数据所对应的sheet数组下标
def CaculateEMA_12(row):
    if row < 0:
        print("输入有误！请重新输入")
        return -1
    if row >= sheet.nrows:
        print("输入有误！请重新输入")
        return -1
    if row == 1:  # 递归初始值为当天（第一天）收盘价
        return sheet.cell_value(row, 4)
    return CaculateEMA_12(row - 1) * 11 / 13 + sheet.cell_value(row, 4) * 2 / 13

# 递归函数，计算26日EMA，计算公式：EMA（26）=前一日的EMA(26)×25÷27+今日收盘价×2÷27
# 参数row为当前日期数据所对应的sheet数组下标
def CaculateEMA_26(row):
    if row < 0:
        print("输入有误！请重新输入")
        return -1
    if row >= sheet.nrows:
        print("输入有误！请重新输入")
        return -1
    if row == 1:  # 递归初始值为当天（第一天）收盘价
        return sheet.cell_value(row, 4)
    return CaculateEMA_12(row - 1) * 25 / 27 + sheet.cell_value(row, 4) * 2 / 27

# 递归函数，计算平滑移动平均值DEA
# 参数row为当前日期数据所对应的sheet数组下标
def CaculateDEA(row):
    if row < 0:
        print("输入有误！请重新输入")
        return -1
    if row >= sheet.nrows:
        print("输入有误！请重新输入")
        return -1
    if row == 1:  # 递归初始值为当天（第一天）DIFF值，差离值DIFF = EMA(12) – EMA(26)
        return CaculateEMA_12(row) - CaculateEMA_26(row)
    return (CaculateEMA_12(row) - CaculateEMA_26(row)) * 2 / (9 + 1) + CaculateDEA(row - 1) * (9 - 1) / (9 + 1)

# 分析RSI背离情况的函数
# 参数trend为上升趋势和下降趋势，上升为0，下降为1
# 参数day为上升|下降趋势所在的时间范围
def RSIanalyze(trend, day):
    # 判断趋势输入合不合法
    if trend != 1 and trend != 0:
        return
    # 判断day是否合法
    if day >= sheet.nrows or (DateRow - day) <= 1:
        print("RSI分析中，时间范围不正确")
        return -1
    if trend == 1:
        maxRow = 0 # 收盘价最高点所在行数
        for rown in range(DateRow - day, DateRow - 1):
            if sheet.cell_value(rown, 4) < sheet.cell_value(rown + 1, 4):
                maxRow = rown + 1
            else:
                maxRow = rown
        if CaculateRSI(DateRow) < CaculateRSI(maxRow):
            print("上升趋势中，新的收盘价高点对应的RSI值低于旧收盘价高点对应的RSI值")
    if trend == 0:
        minRow = 0 # 收盘价最低点所在行数
        for rown in range(DateRow - day, DateRow - 1):
            if sheet.cell_value(rown, 4) > sheet.cell_value(rown + 1, 4):
                minRow = rown + 1
            else:
                minRow = rown
        if CaculateRSI(DateRow) > CaculateRSI(minRow):
            print("下降趋势中，新的收盘价低点对应RSI值高于旧收盘价低点对应的RSI值")


if __name__ == '__main__':
    global workbook, sheet_name, sheet  # 全局变量
    # 打开测试数据excel
    workbook = xlrd.open_workbook('F:\\javaproject\\analyze\\testData.xlsx')
    print('读取成功')
    # 获取所有sheet
    sheet_name = workbook.sheet_names()[0]

    # 根据sheet索引或者名称获取sheet内容
    sheet = workbook.sheet_by_index(0)  # sheet索引从0开始

    # sheet的名称，行数，列数
    print(sheet.name, sheet.nrows, sheet.ncols)

    # 读取用户输入的日期，确定用户需要的数据
    SwitchTime()

    # 计算RSI值
    RSI = CaculateRSI()
    # 计算EMA(12)和EMA(16)
    EMA_12 = CaculateEMA_12(DateRow - 1)
    print("当天EMA(12)值为：", EMA_12)
    EMA_26 = CaculateEMA_26(DateRow - 1)
    print("当天EMA(26)值为：", EMA_26)
    # 计算差离值
    DIFF = EMA_12 - EMA_26
    # 计算DEA
    DEA = CaculateDEA(DateRow - 1)
    # 计算MACD动能柱值 = DIFF – DEA
    MACD = DIFF - DEA
    if DateRow == 2:  # 考虑初始MACD动能柱情况，在此之前无MACD值
        if MACD < 0:  # 如果初始小于0，向下穿越
            print("向下穿越")
        if MACD > 0:  # 如果初始大于0，向上穿越
            print("向上穿越")
    else:
        # 计算前一天MACD值
        MACD_before = CaculateEMA_12(DateRow - 2) - CaculateEMA_26(DateRow - 2) - CaculateDEA(DateRow - 2)
        print(MACD_before)
        if MACD_before < 0 and MACD > 0:  # 前一天MACD值小于0，今天MACD值大于0，向上穿越
            print("向上穿越")
        if MACD_before > 0 and MACD < 0:  # 前一天MACD值大于0，今天MACD值小于0，向下穿越
            print("向下穿越")

    RSIanalyze(1, 200)