from collections import deque
import numpy as np
from datetime import datetime

now = datetime.now().strftime('%Y%m%d')
print(now)

n_1 = 0
n_0 = 0
for i in range(0,100):
    ss = np.random.choice(np.arange(0,2), p=[0.4, 0.6])
    if ss == 0:
        n_0 +=1
    elif ss == 1:
        n_1 += 1

print(n_1)
print(n_0)