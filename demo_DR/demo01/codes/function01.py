import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import dataReader

file_path = "../testData.xlsx"
df = dataReader.getDataFrame( file_path )

#   print( df )
L = 10

#   basic data
rows = df.shape[0]
columns = df.shape[1]
total_date = df['time']
high_price = df['HIGH']
low_price = df['LOW']

'''
x       ->  time/NO.
high    ->  highest
low     ->  lowest
'''
x = []
high = []
low = []
data_low ={}  #   字典存储 key -> (low,high)
data_high = {}

#   get highest/lowest for each certain date
def getHighAndLow(index):
    highest = high_price[index]
    lowest = low_price[index]
    low_date = total_date[index]
    high_date = total_date[index]

    for i in (0,L-1):
       
        #   get data that is L days earlier
        highest = max( high_price[index-i],highest )
        lowest = min( low_price[index-i],lowest )
        if highest < high_price[index-i] :
            highest = high_price[index-i]
            high_date = total_date[index-i]
        if lowest > low_price[index-i] :
            lowest = low_price[index-i]
            low_date = total_date[index-i]

    #return highest,lowest    
    return (low_date,lowest),(high_date,highest)

#   step 1: recording highest and lowest data
def hlRecording():
    i = rows-1
    end_i = i - 3*L
    num = 0

    while i >= end_i:
        num = num+1
        (low_index,low_tmp_data),(high_index,high_tmp_data) = getHighAndLow( i )
        high.append(high_tmp_data)
        low.append(low_tmp_data)
        i = i-1

        #   judge if data can be added into the dict
        if low_index not in data_low :
            #   add
            data_low[low_index] = low_tmp_data
        else:
            print( "Repeat!" )
        if high_index not in data_high :
            #   add
            data_high[high_index] = high_tmp_data
        else:
            print( "Repeat!" )

    ascendingOrder()

    # print( data_high )
    # print( data_low )
    print( "X:" + str(len(x)) )
    print( "low:" + str(len(data_low)) )
    print( "high:" + str(len(data_high)) )

    # for j in range( 0,num ):
    #     x.append(j)
    #   visualize and paint
    # plt.plot( x,high )
    # plt.plot( x,low )
    # plt.show()

#   ascending -> 2 dicts
def ascendingOrder():
    global data_low
    global data_high
    low_list = list( data_low.items() )
    low_list.sort()
    data_low = dict( low_list )

    high_list = list( data_high.items() )
    high_list.sort()
    data_high = dict( high_list )

#   step 2: get top and bottom data
#   find top data
def selectedData(data_dict,flag):
    size = len( data_dict )
    keys = list( data_dict.keys() )
    values = list( data_dict.values() )
    x = []
    data_save = []

    if flag == True:
        #   top data
        for i in range( 1,size-1 ):
            # judge if top data
            if values[i] >= values[i-1] and values[i] > values[i+1]:
                data_save.append( values[i] ) 
    else:
        #   bottom data
        for i in range( 1,size-1 ):
            #   judge if low data
            if values[i] <= values[i-1] and values[i] < values[i+1]:
                data_save.append( values[i] )
    #   end if
    for i in range(0,len(data_save)):
        x.append(i+1)
    return x,data_save


def getTopData(data_high):
    x,top = selectedData( data_high,True )
    return x,top
    
def getBottomData( data_low ):
    x,bottom = selectedData( data_low,False )
    return x,bottom

def paintTopAndBottom():
    x,top = getTopData(data_high)
    y,bottom = getBottomData(data_low)
    plt.plot( x,top )
    plt.plot( y,bottom )
    plt.show()


#-----------------testing-----------------#
hlRecording()
paintTopAndBottom()