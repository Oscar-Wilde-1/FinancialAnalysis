import xlrd
import datetime
import operator

data = xlrd.open_workbook('D:\\testData.xlsx')
table = data.sheet_by_name('Sheet1')


# 实际日期函数转换为Excel中日期表示，并在表格中查找对应日期所在行数

def date_transform():
    year = int(input("输入年："))
    month = int(input("输入月："))
    day = int(input("输入日："))
    rows = -1
    if year < 1 or month < 1 or month > 12 or day < 1 or day > 31:
        print("请输入合理的日期")
        return rows
    date_num_in_excel = (datetime.date(year, month, day) - datetime.date(1900, 1, 1)).days + 2
    temp_row = -1
    for temp_row in range(1, table.nrows):
        if int(table.cell_value(temp_row, 0)) == date_num_in_excel:
            rows = temp_row
            break
    if rows == -1:
        print('输入的日期在数据中不存在')
    return rows


# 读取对应日期的最高点
def read_high(row_number):
    return table.cell_value(row_number, 2)


# 读取对应日期的最低点
def read_low(row_number):
    return table.cell_value(row_number, 3)


# 读取对应日期的收盘价
def read_close(row_number):
    return table.cell_value(row_number, 4)


# 判断数组是否为升序排列
def is_ascending_order(ls):
    flag = True
    for i in range(1, len(list(ls))):
        if ls[i] < ls[i - 1]:
            flag = False
            break
    return flag


# 判断数组是否为升序排列
def is_descending_order(ls):
    flag = True
    for i in range(1, len(list(ls))):
        if ls[i] > ls[i - 1]:
            flag = False
            break
    return flag


# 返回从start位置向前的一个周期内最高的HIGH值
def read_one_cycle_high(cycle, start):
    max_HIGH = 0.0
    for i in range(start - cycle + 1, start + 1):
        if read_high(i) > max_HIGH:
            max_HIGH = read_high(i)
    return max_HIGH


# 返回从start位置向前的一个周期内最小的LOW值
def read_one_cycle_low(cycle, start):
    min_LOW = read_low(start - cycle + 1)
    for i in range(start - cycle + 1, start + 1):
        if read_low(i) < min_LOW:
            min_LOW = read_low(i)
    return min_LOW


# 迭代求解每一次的MAX_HIGH，并记录是否为重复点
def read_max_by_step(cycle, start):
    # pre_max_high指前一个周期长度内计算出的最高点
    # 计算初始周期内的MAX_HIGH值，作为pre_max_high的初始值
    pre_max_high = read_one_cycle_high(cycle, start)
    # 存储MAX_HIGH数组,数组中不会出现重复的MAX_HIGH值，因为重复出现的被判断到后就不会记录在数组中
    MAX_HIGH = [pre_max_high]

    # 记录每一次的最高点是否重复,1表示重复，0表示没有
    MAX_REPEAT = [0]
    for current_location in range(start - cycle, start - 3 * cycle - cycle, -1):
        current_high = read_high(current_location)
        # 如果上一次的MAX_HIGH值出现在此次被除去的日期中
        if read_high(current_location + cycle) == pre_max_high:
            # 若新引进日期当天的HIGH值高于pre_max_high
            if current_high > pre_max_high:
                MAX_HIGH.append(current_high)
                pre_max_high = current_high
                MAX_REPEAT.append(0)
            else:
                new_max_high = read_one_cycle_high(cycle, current_location + cycle - 1)
                if new_max_high != pre_max_high:
                    pre_max_high = new_max_high
                    MAX_HIGH.append(pre_max_high)
                    MAX_REPEAT.append(0)
                else:
                    MAX_REPEAT.append(1)

        # 如果上一次MAX_HIGH不在被除去的周期中，即仍处于移动后的新周期内
        else:
            if current_high > pre_max_high:
                MAX_HIGH.append(current_high)
                pre_max_high = current_high
                MAX_REPEAT.append(0)
            else:
                MAX_REPEAT.append(1)
    return MAX_REPEAT, MAX_HIGH


def read_min_by_step(cycle, start):
    # pre_min_low指前一个周期长度内计算出的最低点
    # 计算初始周期内的MIN_LOW值，作为pre_min_low的初始值
    pre_min_low = read_one_cycle_low(cycle, start)
    # 存储MIN_LOW数组,数组中不会出现重复的MIN_LOW值，因为重复出现的被判断到后就不会记录在数组中
    MIN_LOW = [pre_min_low]

    # 记录每一次的最高点是否重复,1表示重复，0表示没有
    MIN_REPEAT = [0]
    for current_location in range(start - cycle, start - 3 * cycle - cycle, -1):
        current_low = read_low(current_location)
        # 如果上一次的MIN_LOW值出现在此次被除去的日期中
        if read_low(current_location + cycle) == pre_min_low:
            # 若新引进日期当天的LOW值小于pre_min_low
            if current_low < pre_min_low:
                MIN_LOW.append(current_low)
                pre_min_low = current_low
                MIN_REPEAT.append(0)
            else:
                new_min_low = read_one_cycle_low(cycle, current_location + cycle - 1)
                if new_min_low != pre_min_low:
                    pre_min_low = new_min_low
                    MIN_LOW.append(pre_min_low)
                    MIN_REPEAT.append(0)
                else:
                    MIN_REPEAT.append(1)

        # 如果上一次MIN_LOW不在被除去的周期中，即仍处于移动后的新周期内
        else:
            if current_low < pre_min_low:
                MIN_LOW.append(current_low)
                pre_min_low = current_low
                MIN_REPEAT.append(0)
            else:
                MIN_REPEAT.append(1)
    return MIN_REPEAT, MIN_LOW


# 去除连续高点中的最高点和连续低点中的最低点
def continuity_eliminate(MIN_REPEAT, MIN_LOW, MAX_REPEAT, MAX_HIGH):
    MAX_HIGH_WITHOUT_CONTINUITY = []
    MIN_LOW_WITHOUT_CONTINUITY = []
    max_flag = 0
    min_flag = 0
    min_repeat_len = len(list(MIN_REPEAT))
    max_repeat_len = len(list(MAX_REPEAT))
    for i in range(0, min_repeat_len):
        # 第一位为0，非第一位的0且左边为1，最后一位为0
        if i == 0 or (MIN_REPEAT[i] == 0 and MIN_REPEAT[i - 1] != 0):
            start_location = i
            move_location = i
            while MIN_REPEAT[move_location] == 0 and move_location < min_repeat_len - 1:
                move_location = move_location + 1
            # 0的连续个数大于1，或有连续两个0在最右侧，导致move-start值等于1但是有连续两个0
            if move_location - start_location > 1 or (
                    move_location - start_location == 1 and move_location == min_repeat_len - 1):
                temp = []
                for j in range(min_flag, min_flag + move_location - start_location):
                    temp.append(MIN_LOW[j])
                min_flag = min_flag + move_location - start_location
                MIN_LOW_WITHOUT_CONTINUITY.append(min(temp))

            else:

                MIN_LOW_WITHOUT_CONTINUITY.append(MIN_LOW[min_flag])
                min_flag = min_flag + 1

    for i in range(0, max_repeat_len):
        if i == 0 or (MAX_REPEAT[i] == 0 and MAX_REPEAT[i - 1] != 0):
            start_location = i
            move_location = i
            while MAX_REPEAT[move_location] == 0 and move_location < max_repeat_len - 1:
                move_location = move_location + 1
            if move_location - start_location > 1 or (
                    move_location - start_location == 1 and move_location == max_repeat_len - 1):
                temp = []
                for j in range(max_flag, max_flag + move_location - start_location):
                    temp.append(MAX_HIGH[j])
                max_flag = max_flag + move_location - start_location
                MAX_HIGH_WITHOUT_CONTINUITY.append(max(temp))

            else:
                MAX_HIGH_WITHOUT_CONTINUITY.append(MAX_HIGH[max_flag])

                max_flag = max_flag + 1

    # print(MAX_HIGH_WITHOUT_CONTINUITY)
    # print(MIN_LOW_WITHOUT_CONTINUITY)
    return MAX_HIGH_WITHOUT_CONTINUITY, MIN_LOW_WITHOUT_CONTINUITY


# 趋势判断
def trend_judgment():
    print("输入当前时点")
    current_row = date_transform()
    cycle = int(input("输入周期长度："))
    while current_row < 4 * cycle:
        print("该时点以前的数据量不足以支持分析，请重新选择更向后的时点")
        current_row = date_transform()
        cycle = int(input("输入周期长度："))
    # 存储计算出的每一个周期长度的数据中最高的HIGH,即高点数组
    tH = []
    # 存储计算出的每一个周期长度的数据中最小的LOW,即低点数组
    tL = []

    # 更改算法，添加重复性判断，取消暴力遍历法
    # for i in range(current_row, current_row - 3 * cycle - 1, -1):
    #     tH.append(read_one_cycle_high(cycle, i))
    #    tL.append(read_one_cycle_low(cycle, i))
    max_high_results = read_max_by_step(cycle, current_row)
    min_low_results = read_min_by_step(cycle, current_row)
    print('MAX_HIGH重复性判断数组：' + str(max_high_results[0]))
    print('MAX_HIGH剔除重复点后的结果数组：' + str(max_high_results[1]))
    print('MIN_LOW重复性判断数组：' + str(min_low_results[0]))
    print('MIN_LOW剔除重复点后的结果数组：' + str(min_low_results[1]))
    results = continuity_eliminate(min_low_results[0], min_low_results[1], max_high_results[0], max_high_results[1])
    print('保留连续高点中最高点后的MAX_HIGH_WITHOUT_CONTINUITY数组' + str(results[0]))
    print('保留连续低点中最低点后的MIN_LOW_WITHOUT_CONTINUITY数组' + str(results[1]))

    # 上升趋势及下降趋势判断
    if is_ascending_order(results[0]) and is_ascending_order(results[1]):
        print("满足上升趋势")
    elif is_descending_order(results[0]) and is_descending_order(results[1]):
        print("满足下降趋势")
    else:
        print("不存在趋势")

    # 向上突破及向下跌破判断

    if read_close(current_row) > results[0][-1]:
        print("向上突破（" + str(results[0][-1]) + "）")
    elif read_close(current_row) > results[1][-1]:
        print("向下跌破（" + str(results[1][-1]) + "）")
    else:
        print("不存在向上突破或向下跌破现象")

    return


if __name__ == '__main__':
    trend_judgment()
