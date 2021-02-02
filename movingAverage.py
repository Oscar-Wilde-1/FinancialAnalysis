#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :movingAverage.py
@说明    :单均线与双均线判断，默认输入参数未天
@时间    :2020/12/07 21:21:31
@作者    :Rui Dong
@版本    :1.0
'''
import pandas as pd

filePath = 'data/testData.xlsx'


def timeConvert(year, month, day):
    '''
    转换时间
    '''
    date = str(year) + "-" + str(month) + "-" + str(day)
    return date


class averageLine:

    def __init__(self, filePath='data/testData.xlsx', year=2020, month=9, day=9):
        #   默认是以天计算
        df = pd.read_excel(filePath)
        date = timeConvert(year, month, day)
        indexVal = df.loc[(df['Unnamed: 0'] == date)]
        self.df = df
        # print( self.df )
        if self.df.empty:
            print("未输入正确的日期！")
            return
        self.close_price = self.df['CLOSE']
        self.date = self.df['Unnamed: 0']
        self.rows = self.df.shape[0] - 1

        self.T = indexVal.index.values[0]
        print(self.close_price[self.T])
        # print(type(self.T))
        self.N = 0
        self.M = 0
        self.doubleN = 0

    #   设置单均线输入的接口
    #   接口，输入依次为周期和
    def setSingelTime(self, N):
        self.N = N

    #   设置双均线的接口
    def setDoubleTime(self, M, N):
        if M < N:
            print("M must > N!")
            return
        self.M = M
        self.doubleN = N

    def getMA(self, T, N):
        '''
        获取n日均线价格平均
        '''
        avg = 0
        for i in range(1, N + 1):
            # print( i )
            avg += self.close_price[T - i]

        return avg / N

    def singleAverageCompare(self, T, N):
        '''
        单均线信号标准,P(t) v.s P(t-1)
        '''
        MA_T = self.getMA(T, N)
        MA_Tpre = self.getMA(T - 1, N)
        # print( MA_T )
        # print( MA_Tpre )
        P_close = self.close_price[T]
        Ppre_close = self.close_price[T - 1]
        # print( P_close )
        # print( Ppre_close )
        return self.singleAverageCheck(T, MA_T, MA_Tpre, P_close, Ppre_close)

    def singleAverageCheck(self, T, MA_T, MA_Tpre, P_close, Ppre_close):
        '''
        单均线判断是向上还是向下
        '''
        if MA_T > MA_Tpre and (MA_T > P_close and Ppre_close < MA_Tpre):
            date = self.date[T]
            res = str(date.year) + "/" + str(date.month) + "/" + str(date.day) + ": %d 日单均线判断：向下穿越，提示卖出！\n"%(self.N)
            print(res)
            return res

        elif MA_T < MA_Tpre and (MA_T < P_close and Ppre_close > MA_Tpre):
            date = self.date[T]
            res = str(date.year) + "/" + str(date.month) + "/" + str(date.day) + ": %d 日单均线判断：向上穿越，提示买入！\n"%(self.N)
            print(res)
            return res
        else:
            # print( "单均线判断：无明显穿越情况\n" )
            return ""

    def doubleAveraqgeCompare(self, T, M, N):
        '''
        双均线技术指标
        '''
        if M <= N:
            print("M must > N !")
            return

        MA_T_m = self.getMA(T, M)
        MA_T_mpre = self.getMA(T - 1, M)
        MA_T_n = self.getMA(T, N)
        MA_T_npre = self.getMA(T - 1, N)
        return self.doubleAveraqgeCheck(T, M, N, MA_T_m, MA_T_mpre, MA_T_n, MA_T_npre)

    def doubleAveraqgeCheck(self, T, M, N, Ptm, Ptm_pre, Ptn, Ptn_pre):
        '''
        双均线价格比较
        '''
        if Ptm > Ptm_pre and Ptn > Ptn_pre:
            if Ptn_pre < Ptm_pre and Ptn > Ptm_pre:
                date = self.date[T]
                res = str(date.year) + "/" + str(date.month) + "/" + str(date.day) + ": 双均线判断：%d 日均线向上穿越 %d 日均线，提示买入！\n" % (N, M)
                print(res)
                return res
        if Ptm < Ptm_pre and Ptn < Ptn_pre:
            date = self.date[T]
            res = str(date.year) + "/" + str(date.month) + "/" + str(date.day) + ": 双均线判断：%d 日均线向下穿越 %d 日均线，提示卖出！\n" % (N, M)
            print(res)
            return res
        else:
            #res = str("双均线判断：无明显穿越情况")
            # print("双均线判断：无明显穿越情况\n")
            # return res
            return ""

    #   输出接口
    def averageOutput(self):
        '''
        返回两个记录数组
        '''
        res1 = []
        res2 = []
        for i in range(0, (self.T - self.N)):
            res = self.singleAverageCompare(self.T - i, self.N)
            if len(res) > 0:
                res1.append(res)
                res1.append("\n")
        # res1 = self.singleAverageCompare( self.T,self.N )
        for j in range(0, self.T - self.M):
            res = self.doubleAveraqgeCompare(self.T - j, self.M, self.doubleN)
            if len(res) > 0:
                res2.append(res)
                res2.append("\n")
        return res1[:-1], res2[:-1]
