#判断字典中某个键是否存在
arr = {"int":"整数","float":"浮点","str":"字符串","list":"列表","tuple":"元组","dict":"字典","set":"集合"}
#使用 in 方法
if "int" in arr:
    print("存在")
if "float" in arr.keys():
    print("存在")
#判断键不存在
if "floats" not in arr:
    print("不存在")
if "floats" not in arr:
    print("不存在")