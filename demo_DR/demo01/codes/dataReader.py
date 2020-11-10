import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#df = pd.read_excel( file_path,encoding='gbk' )

# date = np.array( df['time'] )
# print(type(date[0]))


#   get dataFrame
def getDataFrame( file_path ):
    df = pd.read_excel( file_path,encoding='gbk' )
    return df
