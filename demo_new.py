'''
如何使用python快读统计列表中重复项出现的次数?

这个问题在实际应用场景中使用频率比较广泛。本文讲解一下常用的方法:
'''

# 第一种使用标准库提供的collections:

from collections import Counter
import numpy as np
num=1000000
lst = np.random.randint(num / 10, size=num)
res = Counter(lst)    # 返回的值是字典格式如{'xx':8,'xxx':9}
Counter(words).most_common(4)    # 输出的是出现次数最后的数据如[('xxx', 8), ('xxx', 5),]


# 第二种使用numpy模块(更快)

import numpy
num=1000000
lst = np.random.randint(num / 10, size=num)
dict(zip(*np.unique(lst, return_counts=True)))

# 第三种使用list.count()方法(最慢)

import numpy
num=1000000
lst = np.random.randint(num / 10, size=num)
dic = {}
for i in lst:
    dic[i] = lst.count(i)