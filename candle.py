import pandas as pd


# author 刘钰
from trend import Trend


class Candle:

    # 判断形态
    @staticmethod
    def judge(year, month, day, _year, _month, _day, cycle):
        string = ''

        # 打开文件，获取excel文件的workbook（工作簿）对象
        workbook = pd.DataFrame(pd.read_excel("D:/aaa/data/testData1.xlsx"))
        workbook.columns = ['datetime', 'Open', 'High', 'Low', 'Close']

        time1 = pd.Timestamp(year, month, day)
        time2 = pd.Timestamp(_year, _month, _day)
        workbook = workbook.loc[workbook['datetime'] >= time1]
        workbook = workbook.loc[workbook['datetime'] <= time2]
        if workbook.shape[0] < 2:
            string = "输入的时间段内数据少于两条，无法判断形态！"
            return string

        flag = True
        # 获取两天开收盘价的高低情况以判断吞没
        for i in range(1, workbook.shape[0]):
            if workbook.iloc[i - 1][1] > workbook.iloc[i - 1][4]:
                high0 = workbook.iloc[i - 1][1]
                low0 = workbook.iloc[i - 1][4]
            else:
                high0 = workbook.iloc[i - 1][4]
                low0 = workbook.iloc[i - 1][1]

            if workbook.iloc[i][1] > workbook.iloc[i][4]:
                high1 = workbook.iloc[i][1]
                low1 = workbook.iloc[i][4]
            else:
                high1 = workbook.iloc[i][4]
                low1 = workbook.iloc[i][1]

            # 如果呈现吞没形态
            if high1 > high0 and low1 < low0:
                # 判断趋势

                date = workbook.iloc[i - 1][0]
                trend = Trend.judgeTrend(date.year, date.month, date.day, cycle)
                date = workbook.iloc[i][0]
                if trend == 1:
                    string = string + (str(date.year) + "/" + str(date.month) + "/" + str(date.day) + "  看跌吞没\n")
                elif trend == 2:
                    string = string + (str(date.year) + "/" + str(date.month) + "/" + str(date.day) + "  看涨吞没\n")
                flag = False

            # 乌云盖顶
            if workbook.iloc[i][1] > workbook.iloc[i - 1][2] and workbook.iloc[i][4] < (
                    workbook.iloc[i - 1][1] + workbook.iloc[i - 1][4]) / 2:
                # 判断趋势
                date = workbook.iloc[i - 1][0]
                if Trend.judgeTrend(date.year, date.month, date.day, cycle) == 1:
                    date = workbook.iloc[i][0]
                    string = string + (str(date.year) + "/" + str(date.month) + "/" + str(date.day) + "  乌云盖顶\n")
                flag = False

        if flag:
            string = string + "该段时间内无形态\n"

        return string[:-1]
