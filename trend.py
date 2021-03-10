import pandas as pd

dataFrame = pd.read_excel('data/testData.xlsx')
dateIndex = -1
columnName_1 = 'Unnamed: 0'  # 第一列列名
columnName_2 = 'OPEN'  # 第二列列名
columnName_3 = 'HIGH'  # 第三列列名
columnName_4 = 'LOW'  # 第四列列名
columnName_5 = 'CLOSE'  # 第五列列名
inputCycle = 0


# zmx
class Trend:
    # 根据规则，第一条数据的对应位置设置为1，而不是从0开始
    @staticmethod
    def switchTime(year, month, day, tempCycle):
        dateStr = str(year) + "-" + str(month) + "-" + str(day)
        df1 = dataFrame.loc[(dataFrame[columnName_1] == dateStr)]
        if df1.empty:
            print("输入日期错误！请重新输入！")
            return False
        else:
            tempDate = df1.index[0] + 1
            # 输入日期之前的数据量应满足在该周期下的分析所需数
            if tempDate < 4 * tempCycle:
                print("该日期之前的数据量不足以进行分析！请重新输入！")
                return False
            else:
                global dateIndex
                dateIndex = tempDate
                global inputCycle
                inputCycle = tempCycle
        return True

    # 根据日期返回行号
    @staticmethod
    def read_row_by_date(date):
        df1 = dataFrame.loc[(dataFrame[columnName_1] == date)]
        row = df1.index[0]
        return row

    # 读取第row_number条数据的对应日期
    @staticmethod
    def read_date(row_number):
        return dataFrame.loc[row_number - 1][0]

    # 读取第row_number条数据的最高点，传进来的row_number为1，则代表第一条数据
    @staticmethod
    def read_high(row_number):
        return dataFrame.loc[row_number - 1][2]

    # 读取第row_number条数据的最低点
    @staticmethod
    def read_low(row_number):
        return dataFrame.loc[row_number - 1][3]

    # 读取对应日期的收盘价
    @staticmethod
    def read_close(row_number):
        return dataFrame.loc[row_number - 1][4]

    # 判断数组是否为升序排列
    @staticmethod
    def is_ascending_order(ls):
        flag = True
        if len(ls) == 1:
            return True
        for i in range(1, len(list(ls))):
            if ls[i] < ls[i - 1]:
                flag = False
                break
        return flag

    # 判断数组是否为升降序排列
    @staticmethod
    def is_descending_order(ls):
        flag = True
        for i in range(1, len(list(ls))):
            if ls[i] > ls[i - 1]:
                flag = False
                break
        return flag

    # 返回从start位置(第start条数据)向前的一个周期内最高的HIGH值,以及对应这一天的日期
    @staticmethod
    def read_one_cycle_high(cycle, start):
        max_HIGH = dataFrame.iloc[start - cycle:start, 2].max()
        # DATE = dataFrame[(dataFrame['HIGH'] == max_HIGH)].index.tolist()
        # max_HIGH值出现的位置，由此寻找对应日期，默认如果在该周期内出现多个同样大的max_HIGH，选择离当前时间最近的
        max_HIGH_loc = dataFrame.loc[(dataFrame['HIGH'] == max_HIGH) & (dataFrame.index >= start - cycle) & (
                dataFrame.index <= start - 1), :].index.max()
        max_HIGH_DATE = dataFrame.loc[max_HIGH_loc][0]
        return max_HIGH, max_HIGH_DATE

    # 返回从start位置(第start条数据)向前的一个周期内最小的LOW值
    @staticmethod
    def read_one_cycle_low(cycle, start):
        min_LOW = dataFrame.iloc[start - cycle:start, 3].min()
        min_LOW_loc = dataFrame.loc[(dataFrame['LOW'] == min_LOW) & (dataFrame.index >= start - cycle) & (
                dataFrame.index <= start - 1), :].index.max()
        min_LOW_DATE = dataFrame.loc[min_LOW_loc][0]
        return min_LOW, min_LOW_DATE

    # 迭代求解每一次的MAX_HIGH，并记录对应点日期
    @staticmethod
    def read_max_by_step(cycle, start):
        # pre_max_high指前一个周期长度内计算出的最高点
        # 计算初始周期内的MAX_HIGH值，作为pre_max_high的初始值
        ini_max = Trend.read_one_cycle_high(cycle, start)
        pre_max_high = ini_max[0]
        pre_max_date = ini_max[1]
        # 存储max_HIGH的数组,数组中只记录日期未发生重复时所有对应的max_HIGH值
        MAX_HIGH = [pre_max_high]
        # 用于存储所有未重复的日期
        MAX_HIGH_DATE = [pre_max_date]
        for current_location in range(start - cycle, start - 3 * cycle - cycle, -1):
            current_high = Trend.read_high(current_location)
            current_date = Trend.read_date(current_location)
            # 若新引进日期当天的HIGH值高于pre_max_high
            if current_high > pre_max_high:
                MAX_HIGH.append(current_high)
                MAX_HIGH_DATE.append(current_date)
                pre_max_high = current_high
                pre_max_date = current_date
            else:
                new_max = Trend.read_one_cycle_high(cycle, current_location + cycle - 1)
                new_max_high = new_max[0]
                new_max_date = new_max[1]
                if new_max_date != pre_max_date:
                    MAX_HIGH.append(new_max_high)
                    MAX_HIGH_DATE.append(new_max_date)
                    pre_max_high = new_max_high
                    pre_max_date = new_max_date
        # 将结果按时间顺序排序，将原数组倒序即可
        MAX_HIGH.reverse()
        MAX_HIGH_DATE.reverse()
        return MAX_HIGH, MAX_HIGH_DATE

    @staticmethod
    def read_min_by_step(cycle, start):
        ini_min = Trend.read_one_cycle_low(cycle, start)
        pre_min_low = ini_min[0]
        pre_min_date = ini_min[1]
        MIN_LOW = [pre_min_low]
        MIN_LOW_DATE = [pre_min_date]
        for current_location in range(start - cycle, start - 3 * cycle - cycle, -1):
            current_low = Trend.read_low(current_location)
            current_date = Trend.read_date(current_location)
            # 若新引进日期当天的HIGH值高于pre_max_high
            if current_low < pre_min_low:
                MIN_LOW.append(current_low)
                MIN_LOW_DATE.append(current_date)
                pre_min_low = current_low
                pre_min_date = current_date
            else:
                new_min = Trend.read_one_cycle_low(cycle, current_location + cycle - 1)
                new_min_low = new_min[0]
                new_min_date = new_min[1]
                if new_min_date != pre_min_date:
                    MIN_LOW.append(new_min_low)
                    MIN_LOW_DATE.append(new_min_date)
                    pre_min_low = new_min_low
                    pre_min_date = new_min_date
        MIN_LOW.reverse()
        MIN_LOW_DATE.reverse()
        return MIN_LOW, MIN_LOW_DATE

    @staticmethod
    def continuity_eliminate(MIN_LOW, MAX_HIGH, MIN_LOW_DATE, MAX_HIGH_DATE):
        # 根据DATE中的时间，按时间顺序将高点和低点对应的两个DATE数组合并，同时用不同的标识符进行区分
        # 用以记录两数组分别移动到的位置
        min_flag = 0
        max_flag = 0
        # 合并数组,数组中的元素只有1、2、3这三种
        # 1代表按时间排序，此处为高点，2表示此处为低点，3表示存在高低两点，它们出现在了同一天
        # 以此数组判定连续性，即对其进行遍历，出现连续的1、3序列则表示有多个高点连续，直到某处出现2，1、3子序列被隔断为止
        # 对低点的连续性判定同理
        SEQUENCE = []
        while max_flag != len(MAX_HIGH_DATE) or min_flag != len(MIN_LOW_DATE):
            # 先考虑当其中某个数组提前遍历完成
            if max_flag == len(MAX_HIGH_DATE):
                min_flag = min_flag + 1
                SEQUENCE.append(2)
            elif min_flag == len(MIN_LOW_DATE):
                max_flag = max_flag + 1
                SEQUENCE.append(1)
            else:
                # 若两数组都还没有被遍历完
                if MAX_HIGH_DATE[max_flag] < MIN_LOW_DATE[min_flag]:
                    max_flag = max_flag + 1
                    SEQUENCE.append(1)
                elif MAX_HIGH_DATE[max_flag] == MIN_LOW_DATE[min_flag]:
                    min_flag = min_flag + 1
                    max_flag = max_flag + 1
                    SEQUENCE.append(3)
                else:
                    min_flag = min_flag + 1
                    SEQUENCE.append(2)
        # 用以存储去除连续后的点组
        MAX_HIGH_WITHOUT_CONTINUITY = []
        MIN_LOW_WITHOUT_CONTINUITY = []
        MAX_HIGH_DATE_WITHOUT_CONTINUITY = []
        MIN_LOW_DATE_WITHOUT_CONTINUITY = []
        # 记录当前子段连续点个数
        move = 0
        # 记录当前连续子段的内容
        sub_sequence = []
        # 记录被操作数组所处位置
        loc = 0
        # 取连续高点最高点
        for i in range(0, len(SEQUENCE), 1):
            if SEQUENCE[i] == 1 or SEQUENCE[i] == 3:
                sub_sequence.append(MAX_HIGH[loc])
                move = move + 1
                loc = loc + 1
            else:
                if move != 0:
                    maxInfo = Trend.max_search(sub_sequence)
                    MAX_HIGH_WITHOUT_CONTINUITY.append(maxInfo[0])
                    MAX_HIGH_DATE_WITHOUT_CONTINUITY.append(MAX_HIGH_DATE[loc - move + maxInfo[1]])
                    move = 0
                    sub_sequence = []
        if len(sub_sequence) > 0:
            maxInfo = Trend.max_search(sub_sequence)
            MAX_HIGH_WITHOUT_CONTINUITY.append(maxInfo[0])
            MAX_HIGH_DATE_WITHOUT_CONTINUITY.append(MAX_HIGH_DATE[loc - move + maxInfo[1]])

        move = 0
        sub_sequence = []
        loc = 0
        # 取连续低点最低点
        for i in range(0, len(SEQUENCE), 1):
            if SEQUENCE[i] == 2 or SEQUENCE[i] == 3:
                sub_sequence.append(MIN_LOW[loc])
                move = move + 1
                loc = loc + 1
            else:
                if move != 0:
                    minInfo = Trend.min_search(sub_sequence)
                    MIN_LOW_WITHOUT_CONTINUITY.append(minInfo[0])
                    MIN_LOW_DATE_WITHOUT_CONTINUITY.append(MIN_LOW_DATE[loc - move + minInfo[1]])
                    move = 0
                    sub_sequence = []
        if len(sub_sequence) > 0:
            minInfo = Trend.min_search(sub_sequence)
            MIN_LOW_WITHOUT_CONTINUITY.append(minInfo[0])
            MIN_LOW_DATE_WITHOUT_CONTINUITY.append(MIN_LOW_DATE[loc - move + minInfo[1]])

        return MAX_HIGH_WITHOUT_CONTINUITY, MIN_LOW_WITHOUT_CONTINUITY, MAX_HIGH_DATE_WITHOUT_CONTINUITY, MIN_LOW_DATE_WITHOUT_CONTINUITY

    # 寻找list中最大值及其下标
    @staticmethod
    def max_search(seq):
        tempMax = -1
        tempLoc = -1
        for i in range(0, len(seq), 1):
            if seq[i] >= tempMax:
                tempMax = seq[i]
                tempLoc = i
        return tempMax, tempLoc

    # 寻找list中最小值及其下标
    @staticmethod
    def min_search(seq):
        tempMin = seq[0]
        tempLoc = 0
        for i in range(1, len(seq), 1):
            if seq[i] <= tempMin:
                tempMin = seq[i]
                tempLoc = i
        return tempMin, tempLoc

    # 在上升趋势或下降趋势出现的情况下，根据高低点数组找到对应上升\下降区间
    @staticmethod
    def trend_interval(MAX_HIGH_DATE_WITHOUT_CONTINUITY, MIN_LOW_DATE_WITHOUT_CONTINUITY):
        # 长度为2的数组，用以记录区间内最早的一天和最迟的一天
        interval = []
        if MAX_HIGH_DATE_WITHOUT_CONTINUITY[0] < MIN_LOW_DATE_WITHOUT_CONTINUITY[0]:
            interval.append(MAX_HIGH_DATE_WITHOUT_CONTINUITY[0])
        else:
            interval.append(MIN_LOW_DATE_WITHOUT_CONTINUITY[0])

        if MAX_HIGH_DATE_WITHOUT_CONTINUITY[-1] > MIN_LOW_DATE_WITHOUT_CONTINUITY[-1]:
            interval.append(MAX_HIGH_DATE_WITHOUT_CONTINUITY[-1])
        else:
            interval.append(MIN_LOW_DATE_WITHOUT_CONTINUITY[-1])

        return interval

    # 趋势判断
    @staticmethod
    def trend_judge(MAX_HIGH_WITHOUT_CONTINUITY, MIN_LOW_WITHOUT_CONTINUITY, MAX_HIGH_DATE_WITHOUT_CONTINUITY,
                    MIN_LOW_DATE_WITHOUT_CONTINUITY):
        interval = []
        if len(MAX_HIGH_WITHOUT_CONTINUITY) == 1 and len(MIN_LOW_WITHOUT_CONTINUITY) == 1:
            print("不存在趋势")
            return 3, interval
        elif len(MAX_HIGH_WITHOUT_CONTINUITY) == 1:
            if Trend.is_ascending_order(MIN_LOW_WITHOUT_CONTINUITY):
                print("满足上升趋势,上升区间为：")
                interval = Trend.trend_interval(MAX_HIGH_DATE_WITHOUT_CONTINUITY, MIN_LOW_DATE_WITHOUT_CONTINUITY)
                print(str(interval[0].year) + "/" + str(interval[0].month) + "/" + str(interval[0].day),
                      str(interval[1].year) + "/" + str(interval[1].month) + "/" + str(interval[1].day))
                return 1, interval
            elif Trend.is_descending_order(MIN_LOW_WITHOUT_CONTINUITY):
                print("满足下降趋势，下降区间为：")
                interval = Trend.trend_interval(MAX_HIGH_DATE_WITHOUT_CONTINUITY, MIN_LOW_DATE_WITHOUT_CONTINUITY)
                print(str(interval[0].year) + "/" + str(interval[0].month) + "/" + str(interval[0].day),
                      str(interval[1].year) + "/" + str(interval[1].month) + "/" + str(interval[1].day))
                return 2, interval
            else:
                print("不存在趋势")
                return 3, interval
        elif len(MIN_LOW_WITHOUT_CONTINUITY) == 1:
            if Trend.is_ascending_order(MAX_HIGH_WITHOUT_CONTINUITY):
                print("满足上升趋势,上升区间为：")
                interval = Trend.trend_interval(MAX_HIGH_DATE_WITHOUT_CONTINUITY, MIN_LOW_DATE_WITHOUT_CONTINUITY)
                print(str(interval[0].year) + "/" + str(interval[0].month) + "/" + str(interval[0].day),
                      str(interval[1].year) + "/" + str(interval[1].month) + "/" + str(interval[1].day))
                return 1, interval
            elif Trend.is_descending_order(MAX_HIGH_WITHOUT_CONTINUITY):
                print("满足下降趋势，下降区间为：")
                interval = Trend.trend_interval(MAX_HIGH_DATE_WITHOUT_CONTINUITY, MIN_LOW_DATE_WITHOUT_CONTINUITY)
                print(str(interval[0].year) + "/" + str(interval[0].month) + "/" + str(interval[0].day),
                      str(interval[1].year) + "/" + str(interval[1].month) + "/" + str(interval[1].day))
                return 2, interval
            else:
                print("不存在趋势")
                return 3, interval
        else:
            if Trend.is_ascending_order(MAX_HIGH_WITHOUT_CONTINUITY) and Trend.is_ascending_order(
                    MIN_LOW_WITHOUT_CONTINUITY):
                print("满足上升趋势,上升区间为：")
                interval = Trend.trend_interval(MAX_HIGH_DATE_WITHOUT_CONTINUITY, MIN_LOW_DATE_WITHOUT_CONTINUITY)
                print(str(interval[0].year) + "/" + str(interval[0].month) + "/" + str(interval[0].day),
                      str(interval[1].year) + "/" + str(interval[1].month) + "/" + str(interval[1].day))
                return 1, interval
            elif Trend.is_descending_order(MAX_HIGH_WITHOUT_CONTINUITY) and Trend.is_descending_order(
                    MIN_LOW_WITHOUT_CONTINUITY):
                print("满足下降趋势，下降区间为：")
                interval = Trend.trend_interval(MAX_HIGH_DATE_WITHOUT_CONTINUITY, MIN_LOW_DATE_WITHOUT_CONTINUITY)
                print(str(interval[0].year) + "/" + str(interval[0].month) + "/" + str(interval[0].day),
                      str(interval[1].year) + "/" + str(interval[1].month) + "/" + str(interval[1].day))
                return 2, interval
            else:
                print("不存在趋势")
                return 3, interval

    # 对数据集内每一天进行趋势分析，合并所有的上升区间及下降区间
    @staticmethod
    def transversal_interval():
        # 数据集中最后一天日期
        last_data = dataFrame.iloc[-1][0]
        last_row = Trend.read_row_by_date(last_data) + 1

        # 上升区间二维数组，内部每一个两位的数组代表一个连续上升区间
        up = []
        # 用以统计日期是否仍然连续的数组，一旦区间不再连续，就将其放入up数组，并清空继续计算
        temp_up = []

        down = []
        temp_down = []
        for i in range(4 * inputCycle, last_row + 1, 1):
            maxInfo = Trend.read_max_by_step(inputCycle, i)
            minInfo = Trend.read_min_by_step(inputCycle, i)
            noContinuity = Trend.continuity_eliminate(minInfo[0], maxInfo[0], minInfo[1], maxInfo[1])
            trend_info = Trend.trend_judge(noContinuity[0], noContinuity[1], noContinuity[2], noContinuity[3])
            interval = trend_info[1]
            if trend_info[0] == 1:
                if len(temp_up) == 0:
                    temp_up.append(interval[0])
                    temp_up.append(interval[1])
                else:
                    if interval[0] > temp_up[1]:
                        # 前后上升区间不再连续，将原来的区间放入大数组，更新当前区间
                        up.append(temp_up)
                        temp_up = []
                        temp_up.append(interval[0])
                        temp_up.append(interval[1])
                    elif interval[1] > temp_up[1]:
                        # 延长连续区间
                        temp_up[1] = interval[1]
            elif trend_info[0] == 2:
                if len(temp_down) == 0:
                    temp_down.append(interval[0])
                    temp_down.append(interval[1])
                else:
                    if interval[0] > temp_down[1]:
                        # 前后上升区间不再连续，将原来的区间放入大数组，更新当前区间
                        down.append(temp_down)
                        temp_down = []
                        temp_down.append(interval[0])
                        temp_down.append(interval[1])
                    elif interval[1] > temp_down[1]:
                        # 延长连续区间
                        temp_down[1] = interval[1]
        if len(temp_up) > 0:
            up.append(temp_up)
        if len(temp_down) > 0:
            down.append(temp_down)

        up_result = "全数据集的上升区间："
        down_result = "全数据集的下降区间："
        for i in range(0, len(up), 1):
            up_result = up_result + str(up[i][0].year) + "/" + str(up[i][0].month) + "/" + str(up[i][0].day) \
                        + "--" + str(up[i][1].year) + "/" + str(up[i][1].month) + "/" + str(up[i][1].day) + "  "

        for i in range(0, len(down), 1):
            down_result = down_result + str(down[i][0].year) + "/" + str(down[i][0].month) + "/" + str(down[i][0].day) \
                          + "--" + str(down[i][1].year) + "/" + str(down[i][1].month) + "/" + str(down[i][1].day) + "  "

        result = up_result + "\n" + down_result
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", result)
        return result

    # 突破判断
    @staticmethod
    def break_judge(MAX_HIGH_WITHOUT_CONTINUITY, MIN_LOW_WITHOUT_CONTINUITY):

        if Trend.read_close(dateIndex) > MAX_HIGH_WITHOUT_CONTINUITY[-1]:
            print("向上突破（" + str(MAX_HIGH_WITHOUT_CONTINUITY[-1]) + "）")
            result1 = str("向上突破（" + str(MAX_HIGH_WITHOUT_CONTINUITY[-1]) + "）")
        else:
            print("不存在向上突破现象")
            result1 = "不存在向上突破现象"

        if Trend.read_close(dateIndex) < MIN_LOW_WITHOUT_CONTINUITY[-1]:
            print("向下跌破（" + str(MIN_LOW_WITHOUT_CONTINUITY[-1]) + "）")
            result2 = str("向下跌破（" + str(MIN_LOW_WITHOUT_CONTINUITY[-1]) + "）")
        else:
            print("不存在向下跌破现象")
            result2 = "不存在向下跌破现象"
        json_result = [result1, result2]
        return result1 + "\n" + result2, json_result

    # 分析流程入口
    @staticmethod
    def analysis(date, cycle):
        global dateIndex
        dateIndex = date
        global inputCycle
        inputCycle = cycle
        result = []
        json_result = []
        maxInfo = Trend.read_max_by_step(inputCycle, dateIndex)
        # print("无重复性的最高点序列如下：")
        # print(maxInfo[0])
        # print("\n无重复性的最高点序列对应日期如下：")
        # print(maxInfo[1])
        minInfo = Trend.read_min_by_step(inputCycle, dateIndex)
        # print("\n无重复性的最低点序列如下：")
        # print(minInfo[0])
        # print("\n无重复性的最低点序列对应日期如下：")
        # print(minInfo[1])
        noContinuity = Trend.continuity_eliminate(minInfo[0], maxInfo[0], minInfo[1], maxInfo[1])
        print("\n无重复性和连续性的最高点序列如下：")
        print(noContinuity[0])
        print("\n无重复性和连续性的最高点序列对应日期如下：")
        print(noContinuity[2])
        print("\n无重复性和连续性的最低点序列如下：")
        print(noContinuity[1])
        print("\n无重复性和连续性的最低点序列对应日期如下：")
        print(noContinuity[3])
        print("\n趋势判断如下：")

        interval = Trend.transversal_interval()

        trendResult = Trend.trend_judge(noContinuity[0], noContinuity[1], noContinuity[2], noContinuity[3])

        if trendResult[0] == 3:
            # result.append(interval + "\n" + "当天不存在趋势")
            result.append("趋势为盘整")
            json_result.append(result)
        elif trendResult[0] == 1:
            # result.append(interval + "\n" + "当天满足上升趋势，上升区间为：" +
            #              str(trendResult[1][0].year) + "/" + str(trendResult[1][0].month) + "/" + str(
            #    trendResult[1][0].day)
            #              + "--" +
            #              str(trendResult[1][1].year) + "/" + str(trendResult[1][1].month) + "/" + str(
            #    trendResult[1][1].day))
            result.append("趋势为上涨")
            json_result.append(result)
        else:
            # result.append(interval + "\n" + "当天满足下降趋势，下降区间为：" +
            #               str(trendResult[1][0].year) + "/" + str(trendResult[1][0].month) + "/" + str(
            #     trendResult[1][0].day)
            #               + "--" +
            #               str(trendResult[1][1].year) + "/" + str(trendResult[1][1].month) + "/" + str(
            #     trendResult[1][1].day))
            result.append("趋势为上涨")
            json_result.append(result)

        print("\n突破判断如下：")
        breakResult, json_breakResult = Trend.break_judge(noContinuity[0], noContinuity[1])
        result.append(breakResult)
        json_result.append(json_breakResult)
        return result, json_result

    # 从最后一个时间点向前遍历，得到所有点对应周期的趋势
    @staticmethod
    def transversal_trend():
        # info为RSI值计算需要的数组
        info = []
        unitInfo = []

        for i in range(4 * inputCycle, dateIndex + 1, 1):
            maxInfo = Trend.read_max_by_step(inputCycle, i)
            minInfo = Trend.read_min_by_step(inputCycle, i)
            noContinuity = Trend.continuity_eliminate(minInfo[0], maxInfo[0], minInfo[1], maxInfo[1])
            if Trend.trend_judge(noContinuity[0], noContinuity[1], noContinuity[2], noContinuity[3])[0] == 1 and len(
                    noContinuity[2]) >= 2:
                unitInfo.append(1)
                unitInfo.append(i - 1)
                unitInfo.append(Trend.read_row_by_date(noContinuity[2][-2]))
                unitInfo.append(Trend.read_row_by_date(noContinuity[2][-1]))
                info.append(unitInfo)
                unitInfo = []
            elif Trend.trend_judge(noContinuity[0], noContinuity[1], noContinuity[2], noContinuity[3])[0] == 2 and len(
                    noContinuity[3]) >= 2:
                unitInfo.append(2)
                unitInfo.append(i - 1)
                unitInfo.append(Trend.read_row_by_date(noContinuity[3][-2]))
                print(Trend.read_row_by_date(noContinuity[3][-2]))
                unitInfo.append(Trend.read_row_by_date(noContinuity[3][-1]))
                info.append(unitInfo)
                unitInfo = []

        return info

    # liuyu接口
    @staticmethod
    def judgeTrend(year, month, day, tempCycle):
        if not Trend.switchTime(year, month, day, tempCycle):
            return 0
        maxInfo = Trend.read_max_by_step(inputCycle, dateIndex)
        minInfo = Trend.read_min_by_step(inputCycle, dateIndex)
        noContinuity = Trend.continuity_eliminate(minInfo[0], maxInfo[0], minInfo[1], maxInfo[1])
        return Trend.trend_judge(noContinuity[0], noContinuity[1], noContinuity[2], noContinuity[3])[0]
