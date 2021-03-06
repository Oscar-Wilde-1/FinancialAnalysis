import pandas as pd
from functools import lru_cache

dataFrame = pd.read_excel('data/testData.xlsx')
DateIndex = -1  # 用户输入的时间对应的数据，所在 *数据数组* 中的下标
RSIday = 0  # 计算RSI值的时间参数
MACDstr = ""  # 分析MACD值得到的分析结果字符串
RSIstr = ""  # 分析RSI背离情况得到的分析结果字符串
DIFF = 0  # 用户输入的日期对应的当天diff值（diff = EMA(12) – EMA(26)）
columnName_1 = 'Unnamed: 0'  # 第一列列名
columnName_2 = 'OPEN'  # 第二列列名
columnName_3 = 'HIGH'  # 第三列列名
columnName_4 = 'LOW'  # 第四列列名
columnName_5 = 'CLOSE'  # 第五列列名
EMA12 = []
EMA26 = []
DEA_arr = []


# 技术指标分析类 zzc
class IndexAnalysis:
    @staticmethod
    # 初始化RSIday
    def InitiallizeRSIday(day):
        global RSIday
        RSIday = day

    @staticmethod
    # 初始化EMA12、EMA26、DEA_arr数组  zzc
    def Initiallize():
        # 初始化EMA12,EMA26,DEA_arr数组
        for index in range(0, dataFrame.shape[0]):
            EMA12.append(IndexAnalysis.CaculateEMA_12(index))
            EMA26.append(IndexAnalysis.CaculateEMA_26(index))
            DEA_arr.append(IndexAnalysis.CaculateDEA(index))
        print("数据表中所有日期的EMA(12),EMA(26),DEA计算完毕\n")
        # print("数据表中所有日期的EMA(12),EMA(26),DEA计算完毕，现在根据MACD指标判断穿越情况：\n")

    @staticmethod
    # 将用户输入的时间转换为excel数据中的行数
    # 参数year month day分别为年，月，日
    def SwitchTime(year, month, day):
        dateStr = str(year) + "-" + str(month) + "-" + str(day)
        df1 = dataFrame.loc[(dataFrame[columnName_1] == dateStr)]
        if df1.empty:
            print("输入日期错误！请重新输入！")
            return False
        else:
            global DateIndex
            DateIndex = df1.index[0]
            return True

    @staticmethod
    # 计算RSI值，zzc
    # 参数index为要计算RSI值的日期，所在 *数据数组* 中的下标
    # 参数RSIday：从用户输入日期开始，day天以内的数据被用来计算RSI值
    def CaculateRSI(dateIndex, day):
        # 判断RSIday是否合法
        if day < 1 or (dateIndex - day) < -1:
            print(dateIndex, day, "时间超过数据存储范围！\n请重新输入合适时间！")
            return -1
        df = dataFrame.loc[dateIndex - day + 1:dateIndex]

        RosePrcie = 0  # day天内，上涨收盘价总和
        FallPrice = 0  # day天内，下跌收盘价总和
        RoseDay = 0  # day天内，上涨的天数
        FallDay = 0  # day天内，下跌的天数
        for row in df.itertuples():
            if getattr(row, columnName_2) > getattr(row, columnName_5):  # 如果收盘价低于开盘价，则该天算做下跌
                # FallPrice += getattr(row, columnName_5)
                FallPrice += getattr(row, columnName_2) - getattr(row, columnName_5)
                FallDay += 1
            else:  # 如果收盘价高于开盘价，则该天算做上涨
                RosePrcie += getattr(row, columnName_5) - getattr(row, columnName_2)
                RoseDay += 1
        # 如果day天内未有下跌收市值(除数为0)，直接返回
        if FallDay == 0:
            print(day, "天内未有下跌收市值(除数为0)请重新输入天数！")
            return -1
        # 如果day天内未有上涨收市值(除数为0)，直接返回
        # if RoseDay == 0:
        # print(day, "天内未有上涨收市值(除数为0)请重新输入天数！")
        # return -1
        # 计算RS值，RS = X天内上涨收市价的平均值  ÷ X天内下跌收市价的平均值
        # RS = (RosePrcie / RoseDay) / (FallPrice / FallDay)
        RS = (RosePrcie / day) / (FallPrice / day)
        # RSI = 100 – (100÷（1+RS）)
        RSI = 100 - (100 / (1 + RS))
        return RSI

    @staticmethod
    @lru_cache(100)
    # 递归函数，计算12日的EMA，计算公式：EMA（12）=前一日的EMA(12)×11÷13+今日收盘价×2÷13  zzc
    # 参数index为要计算EMA_12的日期，所在 *数据数组* 中的下标
    def CaculateEMA_12(index):
        if index < 0:
            print("输入有误！请重新输入")
            return -1
        if index >= dataFrame.shape[0]:
            print("输入有误！请重新输入")
            return -1
        if index == 0:  # 递归初始值为当天（第一天）收盘价
            return dataFrame.loc[index][columnName_5]
        return IndexAnalysis.CaculateEMA_12(index - 1) * 11 / 13 + dataFrame.loc[index][columnName_5] * 2 / 13

    @staticmethod
    @lru_cache(100)
    # 递归函数，计算26日EMA，计算公式：EMA（26）=前一日的EMA(26)×25÷27+今日收盘价×2÷27  zzc
    # 参数index为要计算EMA_26的日期，所在 *数据数组* 中的下标
    def CaculateEMA_26(index):
        if index < 0:
            print("输入有误！请重新输入")
            return -1
        if index >= dataFrame.shape[0]:
            print("输入有误！请重新输入")
            return -1
        if index == 0:  # 递归初始值为当天（第一天）收盘价
            return dataFrame.loc[index][columnName_5]
        return IndexAnalysis.CaculateEMA_26(index - 1) * 25 / 27 + dataFrame.loc[index][columnName_5] * 2 / 27

    @staticmethod
    @lru_cache(100)
    # 递归函数，计算平滑移动平均值DEA  zzc
    # 参数index为要计算DEA的日期，所在 *数据数组* 中的下标
    def CaculateDEA(index):
        if index < 0:
            print("输入有误！请重新输入")
            return -1
        if index >= dataFrame.shape[0]:
            print("输入有误！请重新输入")
            return -1
        if index == 0:  # 递归初始值为当天（第一天）DIFF值，差离值DIFF = EMA(12) – EMA(26)
            # return CaculateEMA_12(index) - CaculateEMA_26(index)
            return EMA12[index] - EMA26[index]
        return (EMA12[index] - EMA26[index]) * 2 / (9 + 1) + IndexAnalysis.CaculateDEA(index - 1) * (9 - 1) / (9 + 1)

    @staticmethod
    # 计算MACD指标 zzc
    # 参数index为要计算DEA的日期，所在 *数据数组* 中的下标
    def MACDanalyze(Index):
        if Index < 0 or Index >= dataFrame.shape[0]:
            print("计算MACD输入有误!")
        # EMA_12 = CaculateEMA_12(Index)
        # EMA_26 = CaculateEMA_26(Index)
        EMA_12 = EMA12[Index]
        EMA_26 = EMA26[Index]
        # 计算差离值
        DIFF = EMA_12 - EMA_26
        # 计算DEA
        DEA = IndexAnalysis.CaculateDEA(Index)
        # 计算MACD动能柱值 = DIFF – DEA
        MACD = DIFF - DEA
        if Index == 0:  # 考虑初始MACD动能柱情况，在此之前无MACD值
            return
        else:
            # 计算前一天MACD值
            # MACD_before = CaculateEMA_12(Index - 1) - CaculateEMA_26(Index - 1) - CaculateDEA(Index - 1)
            MACD_before = EMA12[Index - 1] - EMA26[Index - 1] - DEA_arr[Index - 1]
            # print(MACD_before)
            global MACDstr
            if MACD_before < 0 and MACD > 0:  # 前一天MACD值小于0，今天MACD值大于0，向上穿越
                dataStr = IndexAnalysis.read_date(Index)
                MACDstr += str(dataStr) + " 向上穿越,出现做多机会\n"
                # print("向上穿越")
            if MACD_before > 0 and MACD < 0:  # 前一天MACD值大于0，今天MACD值小于0，向下穿越
                dataStr = IndexAnalysis.read_date(Index)
                MACDstr += str(dataStr) + " 向下穿越,出现做空机会\n"
                # print("向下穿越")

    @staticmethod
    # 分析日线级别RSI背离情况 zzc
    # 参数trend为0，1分别表示上涨和下跌趋势;参数penultimate_index表示倒数第二个高点/低点所在数据数组下标
    # 参数last_index 表示倒数第一个高点/低点所在数据数组下标（上涨趋势中，即trend=0，取高点，反之低点）
    def AnalyzeRSI(trend, penultimate_index, last_index):
        if trend == 0:
            if IndexAnalysis.CaculateRSI(penultimate_index, RSIday) > IndexAnalysis.CaculateRSI(last_index, RSIday):
                print("上升趋势中，新的收盘价高点对应的RSI值低于旧收盘价高点对应的RSI值")
        elif trend == 1:
            if IndexAnalysis.CaculateRSI(penultimate_index, RSIday) < IndexAnalysis.CaculateRSI(last_index, RSIday):
                print("下降趋势中，新的收盘价低点对应RSI值高于旧收盘价低点对应的RSI值")
        else:
            print("计算RSI背离情况中，趋势输入有误")

    @staticmethod
    # 获取在数据数组dataframe中，下标为dataindex的数据的对应日期
    def read_date(dateIndex):
        return (str(dataFrame.loc[dateIndex][0].year) + "/" + str(dataFrame.loc[dateIndex][0].month)
                + "/" + str(dataFrame.loc[dateIndex][0].day))

    @staticmethod
    # 分析RSI背离情况 zzc
    # 参数为zmx提供的数组
    def AnalyzeRSI(trend_array):
        for element in trend_array:
            global RSIstr
            if element[0] == 1:  # 说明处于上升趋势
                # 上升趋势中，新的收盘价高点对应的RSI值低于旧收盘价高点对应的RSI值，给予提示
                if (IndexAnalysis.CaculateRSI(element[2], RSIday)  # element[2]表示倒数第二个高点
                        > IndexAnalysis.CaculateRSI(element[3], RSIday)):  # element[3]表示最后一个高点
                    date = IndexAnalysis.read_date(element[1])
                    RSIstr += date + " 上升趋势中，新的收盘价高点对应的RSI值低于旧收盘价高点对应的RSI值\n"
            elif element[0] == 2:  # 说明处于下降趋势
                # 下降趋势中，新的收盘价低点对应RSI值高于旧收盘价低点对应的RSI值，给予提示
                if (IndexAnalysis.CaculateRSI(element[2], RSIday)  # element[2]表示倒数第二个低点
                        < IndexAnalysis.CaculateRSI(element[3], RSIday)):  # element[3]表示最后一个低点
                    date = IndexAnalysis.read_date(element[1])
                    RSIstr += date + " 下降趋势中，新的收盘价低点对应RSI值高于旧收盘价低点对应的RSI值\n"

    @staticmethod
    # 输出技术指标分析结果 zzc
    def Output():
        IndexAnalysis.Initiallize()
        temStr1 = ""
        for index in range(0, DateIndex + 1):
            # RSI指标保留整数
            RSI = round(IndexAnalysis.CaculateRSI(index, RSIday))
            IndexAnalysis.MACDanalyze(index)
            # 当RSI值大于70时，提示超买。当RSI值小于30时，提示超卖。
            if RSI > 70:
                date = IndexAnalysis.read_date(index)
                temStr1 += str(date) + " RSI值为" + str(RSI) + ",出现做多机会\n"
                # print(temStr1)
                # print("RSI值为：", RSI, "超买")
            elif RSI < 30 and RSI != -1:
                date = IndexAnalysis.read_date(index)
                temStr1 += str(date) + " RSI值为" + str(RSI) + ",出现做空机会\n"
                # print("RSI值为：", RSI, "超卖")
            else:
                temStr1 += ""
                continue

        # print(temStr1)
        result = []
        json_result = []
        if temStr1 == "":
            temStr1 = "无出现做多或做空机会情况\n"
            result.append(temStr1[:-1])
            temStr2 = ["无出现做多或做空机会情况"]
            json_result.append(temStr2)
        else:
            str0 = []
            json_str0 = []
            strList = temStr1.split('\n')  # 用逗号分割str字符串，并保存到列表
            if len(strList) > 5:
                for i in range(-6, -1):
                    # print(111)
                    str0.append(strList[i] + "\n")
                    json_str0.append(strList[i])
            else:
                for i in range(0, len(strList) - 1):
                    # print(222)
                    str0.append(strList[i] + "\n")
                    json_str0.append(strList[i])
            # print(str0)
            # print(json_str0)
            result.append(str0)
            json_result.append(json_str0)

        global RSIstr
        if RSIstr == "":
            RSIstr = "无RSI背离情况\n"
            result.append(RSIstr[:-1])
            RSIStr2 = ["无RSI背离情况"]
            json_result.append(RSIStr2)
        else:
            str0 = []
            json_str0 = []
            strList = RSIstr.split('\n')  # 用逗号分割str字符串，并保存到列表
            if len(strList) > 5:
                for i in range(-6, -1):
                    # print(111)
                    str0.append(strList[i] + "\n")
                    json_str0.append(strList[i])
            else:
                for i in range(0, len(strList) - 1):
                    # print(222)
                    str0.append(strList[i] + "\n")
                    json_str0.append(strList[i])
            # print(str0)
            result.append(str0)
            json_result.append(json_str0)

        global MACDstr
        if MACDstr == "":
            MACDstr = "无向上或向下穿越情况\n"
            result.append(MACDstr[:-1])
            MACDstr2 = ["无向上或向下穿越情况"]
            json_result.append(MACDstr2)
        else:
            str0 = []
            json_str0 = []
            strList = MACDstr.split('\n')  # 用逗号分割str字符串，并保存到列表
            if len(strList) > 5:
                for i in range(-6, -1):
                    # print(MACD111)
                    str0.append(strList[i] + "\n")
                    json_str0.append(strList[i])
            else:
                for i in range(0, len(strList) - 1):
                    # print(MACD222)
                    str0.append(strList[i] + "\n")
                    json_str0.append(strList[i])
            # print(str0)
            result.append(str0)
            json_result.append(json_str0)
        # result.append(MACDstr[:-1])
        return result, json_result
