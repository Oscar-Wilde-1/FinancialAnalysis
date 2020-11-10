#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :function02.py
@说明    :均线模块
@时间    :2020/11/10 11:54:20
@作者    :Rui Dong
@版本    :1.0
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import dataReader

file_path = "../testData.xlsx"
df = dataReader.getDataFrame( file_path )

#   print( df )
L = 10
N = 10
#T = rows-1 # 暂定
#   basic data
rows = df.shape[0]
columns = df.shape[1]
total_date = df['time']
high_price = df['HIGH']
low_price = df['LOW']
close_price = df['CLOSE']
T = rows-1
N = 10

def getMA( T,N ):
    '''
    获取n日均线价格平均
    '''
    #   N days before T
    avg = 0
    for i in range( 0,N-1 ):
        avg += close_price[T-i]

    return avg/N


def singleAverageCompare( T,N ):
    '''
    单均线信号标准,P(t) v.s P(t-1)
    '''
    MA_T = getMA( T,N )
    MA_Tpre = getMA(T-1,N)
    print( MA_T )
    print( MA_Tpre )
    P_close = close_price[T]
    Ppre_close = close_price[T-1]
    print( P_close )
    print( Ppre_close )
    singleAverageCheck( MA_T,MA_Tpre,P_close,Ppre_close )


def singleAverageCheck( MA_T,MA_Tpre, P_close,Ppre_close ):
    '''
    判断是向上还是向下
    '''
    if MA_T > MA_Tpre and ( MA_T > P_close and Ppre_close < MA_Tpre ):
        print( "向下穿越" )
    elif MA_T < MA_Tpre and( MA_T < P_close and Ppre_close > MA_Tpre ):
        print( "向上穿越" )


def doubleAveraqgeCompare( T,M,N ):
    '''
    双均线技术指标
    '''
    if M <= N:
        print( "M must > N !" )
        return
    
    MA_T_m = getMA( T,M )
    MA_T_mpre = getMA( T-1,M )
    MA_T_n = getMA( T,N )
    MA_T_npre = getMA( T-1,N )
    doubleAveraqgeCheck( M,N,MA_T_m,MA_T_mpre,MA_T_n,MA_T_npre )


def doubleAveraqgeCheck( M,N,Ptm,Ptm_pre,Ptn,Ptn_pre ):
    '''
    双均线价格比较
    '''
    if Ptm > Ptm_pre and Ptn > Ptn_pre:
        if Ptn_pre < Ptm_pre and Ptn > Ptm_pre:
            print( "%d 日均线向上穿越 %d 日均线" %( N,M ))
    if Ptm < Ptm_pre and Ptn < Ptn_pre:
         print( "%d 日均线向下穿越 %d 日均线" %( N,M ))


#   testing
if __name__ == "__main__":
    for i in range( 0,10 ):
        singleAverageCompare( T-i,N )
        doubleAveraqgeCompare( T-i,N+10,N )