#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :main.py
@说明    :
@时间    :2020/12/08 20:38:24
@版本    :1.0
'''

import pandas as pd

from RSI1 import IndexAnalysis
from candle import Candle
from report import Report
from trend import Trend
from movingAverage import averageLine

filePath = 'D:/aaa/data/testData1.xlsx'
dataFrame = pd.read_excel(filePath)


def InputInfo():
    year = int(input("输入年: "))
    month = int(input("输入月: "))
    day = int(input("输入日: "))  # 输入需要判断的日期
    tempCycle = int(input("输入周期长度："))  # 输入周期长度
    RSIRange = int(input("请输入用来计算RSI值的时间范围："))  # 输入RSI值的时间范围
    dateStr = str(year) + "-" + str(month) + "-" + str(day)
    NSingle = int(input("输入单均线周期N："))
    MDouble = int(input("输入双均线周期M："))
    NDouble = int(input("输入双均线周期N："))
    df1 = dataFrame.loc[(dataFrame['Unnamed: 0'] == dateStr)]
    if df1.empty:
        print("输入日期错误！请重新输入！")
        InputInfo()
    else:
        tempDate = df1.index[0] + 1
        # 输入日期之前的数据量应满足在该周期下的分析所需数
        if tempDate < 4 * tempCycle:
            print("该日期之前的数据量不足以进行分析！请重新输入！")
            InputInfo()
        else:
            return year, month, day, tempDate, tempCycle, RSIRange, NSingle, MDouble, NDouble


if __name__ == '__main__':
    inputInfo = InputInfo()

    avgLine = averageLine(filePath, inputInfo[0], inputInfo[1], inputInfo[2])
    avgLine.setSingelTime(inputInfo[6])
    avgLine.setDoubleTime(inputInfo[7], inputInfo[8])
    res1, res2 = avgLine.averageOutput()

    array = [Trend.analysis(inputInfo[3], inputInfo[4]),
             Candle.judge(1970, 1, 1, inputInfo[0], inputInfo[1], inputInfo[2], inputInfo[4])]

    IndexAnalysis.SwitchTime(inputInfo[0], inputInfo[1], inputInfo[2])
    IndexAnalysis.InitiallizeRSIday(inputInfo[5])
    IndexAnalysis.AnalyzeRSI(Trend.transversal_trend())

    array.append(IndexAnalysis.Output())
    array.append([res1, res2])

    Report.report(array, inputInfo[0], inputInfo[1], inputInfo[2])
