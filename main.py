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

import time
from movingAverage import averageLine
from flask import Flask, render_template, request, make_response, send_file
from flask_cors import CORS

import json
import os

filePath = 'data/testData.xlsx'
dataFrame = pd.read_excel(filePath)
app = Flask(__name__)

CORS(app, supports_credentials=True)


@app.route('/details', methods=['POST', 'GET'])
def details():
    global array
    workbook = pd.DataFrame(pd.read_excel("data/testData.xlsx"))
    workbook.columns = ['datetime', 'Open', 'High', 'Low', 'Close']
    ret = []
    for i in range(0, workbook.shape[0]):
        ret.append(
            [time.mktime(workbook.iloc[i][0].timetuple()) * 1000 - 28800000, workbook.iloc[i][1], workbook.iloc[i][2],
             workbook.iloc[i][3], workbook.iloc[i][4]])
    errcode = 200
    data = request.get_data()
    data = json.loads(data)
    year = data['year']
    month = data['month']
    day = data['day']  # 获取需要判断的日期
    tempCycle = data['L']  # 获取周期长度
    RSIRange = data['RSI']  # 获取RSI值的时间范围
    dateStr = str(year) + "-" + str(month) + "-" + str(day)
    NSingle = data['NSingle']  # 获取单均线交叉信号判断功能中的单均线周期N
    MDouble = data['MDouble']  # 获取双均线交叉信号判断功能中的双均线周期M
    NDouble = data['NDouble']  # 获取双均线交叉信号判断功能中的双均线周期N

    # 默认值
    if year == 0 and month == 0 and day == 0:
        temp = workbook.iloc[workbook.shape[0] - 1][0]
        year = temp.year
        month = temp.month
        day = temp.day
        tempCycle = 2
        RSIRange = 2
        dateStr = str(year) + "-" + str(month) + "-" + str(day)
        NSingle = 10
        MDouble = 5
        NDouble = 15

    df1 = dataFrame.loc[(dataFrame['Unnamed: 0'] == dateStr)]
    if df1.empty:
        print("输入日期在数据中不存在！请重新输入！")
        errcode = 201
    else:
        tempDate = df1.index[0] + 1
        # 输入日期之前的数据量应满足在该周期下的分析所需数
        if tempDate < 4 * tempCycle:
            print("该日期之前的数据量不足以进行分析！请重新输入！")
            errcode = 202
        elif NDouble <= MDouble:
            errcode = 203
        else:
            try:
                inputInfo = [year, month, day, tempDate, tempCycle, RSIRange, NSingle, MDouble, NDouble]
                avgLine = averageLine(filePath, inputInfo[0], inputInfo[1], inputInfo[2])
            except Exception:
                errcode = 204  # 设置年月日出错
                return {"data": ret, "errcode": errcode}
            try:
                avgLine.setSingelTime(inputInfo[6])
                avgLine.setDoubleTime(inputInfo[7], inputInfo[8])
                res1, res2, json_res1, json_res2 = avgLine.averageOutput()
            except Exception:
                errcode = 205  # 设置均线周期出错
                return {"data": ret, "errcode": errcode}
            try:
                candle_result, candle_json_result = Candle.judge(1970, 1, 1, inputInfo[0], inputInfo[1], inputInfo[2],
                                                                 inputInfo[4])
                trend_result, trend_json_result = Trend.analysis(inputInfo[3], inputInfo[4])
                array = [trend_result, candle_result]

                IndexAnalysis.SwitchTime(inputInfo[0], inputInfo[1], inputInfo[2])
            except Exception:
                errcode = 206  # 设置周期出错
                return {"data": ret, "errcode": errcode}
            try:
                IndexAnalysis.InitiallizeRSIday(inputInfo[5])
                IndexAnalysis.AnalyzeRSI(Trend.transversal_trend())
            except Exception:
                errcode = 207  # 计算rsi值出错
                return {"data": ret, "errcode": errcode}
            try:
                index_result, index_json_result = IndexAnalysis.Output()
                array.append(index_result)
                array.append([res1, res2])
                #  print("!!!!!!!!!!!!!")
                # print(array)
                # Report.report(array, inputInfo[0], inputInfo[1], inputInfo[2])
            except Exception:
                errcode = 208  # 生成报告出错
                return {"data": ret, "errcode": errcode}

    if errcode == 200:
        final_result = {}
        result = json.loads(json.dumps(final_result))
        result['data'] = ret
        result['errcode'] = errcode
        result['form'] = {
            "date1": dateStr,
            "cycle": tempCycle,
            "rsi": RSIRange,
            "n1": NSingle,
            "m": MDouble,
            "n2": NDouble,
            },
        # 生成json数据

        # 对原有array进行变形
        new_array = [[] for _ in range(8)]
        # index_json_result：RSI计算结果
        # candle_json_result：形态提示计算结果
        # json_res1, json_res2；单均线，双均线计算结果
        # trend_json_result:趋势计算结果

        # array重组
        new_array[0].append(trend_json_result[0][0])
        new_array[7].append(trend_json_result[1][0])
        new_array[7].append(trend_json_result[1][1])
        for i in range(0, len(json_res1)):
            new_array[1].append(json_res1[i])
        for i in range(0, len(json_res2)):
            new_array[2].append(json_res2[i])
        for i in range(0, len(index_json_result[0])):
            new_array[3].append(index_json_result[0][i])
        for i in range(0, len(index_json_result[1])):
            new_array[4].append(index_json_result[1][i])
        for i in range(0, len(index_json_result[2])):
            new_array[5].append(index_json_result[2][i])
        for i in range(0, len(candle_json_result)):
            new_array[6].append(candle_json_result[i])

        analysis_result = []

        title = ['趋势', 'N日均线价格穿越情况', 'M日、N日均线交叉和穿越情况', 'RSI指标', 'RSI指标背离情况', 'MACD穿越情况', '形态提示', '前期低点、高点是否突破']
        for i in range(0, len(new_array)):
            unit_info = {}
            unit_info['index'] = str(i)
            unit_info['title'] = title[i]
            subs_info = []
            for j in range(0, len(new_array[i])):
                unit = {}
                unit['title'] = new_array[i][j]
                subs_info.append(unit)
            unit_info['subs'] = subs_info
            analysis_result.append(unit_info)
        result['result'] = analysis_result
        json_result = json.dumps(result, ensure_ascii=False)
        print(json_result)
        return json_result
    else:
        return {"data": ret, "errcode": errcode}


@app.route('/download', methods=['POST', 'GET'])
def download():
    # report_array = [[] for _ in range(8)]
    #
    # download_data = request.get_data()
    # download_data = json.loads(download_data)
    # print(download_data)
    # uid = download_data['UID']
    # download_year = download_data['year']
    # download_month = download_data['month']
    # download_day = download_data['day']
    # result = download_data['result']
    # for i in range(0, len(result)):
    #     unit_dict = {}
    #     unit_dict = result[i]
    #     subs_list = []
    #     subs_list = unit_dict['subs']
    #     for j in range(0, min(5, len(subs_list))):
    #         title_dict = {}
    #         title_dict = subs_list[j]
    #         # print(subs_list[j])
    #         # print(j)
    #         report_array[i].append(title_dict['title'])
    # print("???????????????????")
    # print(report_array)
    # Report.report(report_array, download_year, download_month, download_day, uid)
    # # os.remove('result/report_2021_03_10_12_10_07.docx')
    # string = "result/report_" + uid + ".docx"
    # send_file('data/testData.xlsx')
    return send_file('data/testData.xlsx')


if __name__ == '__main__':
    # inputInfo = InputInfo()
    #
    # avgLine = averageLine(filePath, inputInfo[0], inputInfo[1], inputInfo[2])
    # avgLine.setSingelTime(inputInfo[6])
    # avgLine.setDoubleTime(inputInfo[7], inputInfo[8])
    # res1, res2 = avgLine.averageOutput()
    #
    # array = [Trend.analysis(inputInfo[3], inputInfo[4]),
    #          Candle.judge(1970, 1, 1, inputInfo[0], inputInfo[1], inputInfo[2], inputInfo[4])]
    #
    # IndexAnalysis.SwitchTime(inputInfo[0], inputInfo[1], inputInfo[2])
    # IndexAnalysis.InitiallizeRSIday(inputInfo[5])
    # IndexAnalysis.AnalyzeRSI(Trend.transversal_trend())
    #
    # array.append(IndexAnalysis.Output())
    # array.append([res1, res2])
    #
    # Report.report(array, inputInfo[0], inputInfo[1], inputInfo[2])

    app.run(host='0.0.0.0', port=8081, debug=True)

# def InputInfo():
#     print("请输入当前日期T，程序将会输出从数据集起始日期到当前日期T范围内的技术指标情况。")
#     year = int(input("输入年: "))
#     month = int(input("输入月: "))
#     day = int(input("输入日: "))  # 输入需要判断的日期
#     tempCycle = int(input("输入趋势判断功能中的周期长度L："))  # 输入周期长度
#     RSIRange = int(input("请输入用来计算RSI值的时间范围X："))  # 输入RSI值的时间范围
#     dateStr = str(year) + "-" + str(month) + "-" + str(day)
#     NSingle = int(input("输入单均线交叉信号判断功能中的单均线周期N："))
#     MDouble = int(input("输入双均线交叉信号判断功能中的双均线周期M："))
#     NDouble = int(input("输入双均线交叉信号判断功能中的双均线周期N："))
#     df1 = dataFrame.loc[(dataFrame['Unnamed: 0'] == dateStr)]
#     if df1.empty:
#         print("输入日期错误！请重新输入！")
#         InputInfo()
#     else:
#         tempDate = df1.index[0] + 1
#         # 输入日期之前的数据量应满足在该周期下的分析所需数
#         if tempDate < 4 * tempCycle:
#             print("该日期之前的数据量不足以进行分析！请重新输入！")
#             InputInfo()
#         else:
#             return year, month, day, tempDate, tempCycle, RSIRange, NSingle, MDouble, NDouble
