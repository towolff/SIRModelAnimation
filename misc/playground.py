from collections import deque
import numpy as np


dq = deque(['e', 'e', 'e'])
print(dq)

dq.append('e')
print(dq)
dq.popleft()
print(dq)


print([0] * 10)
print(set(dq))
print(len(set(dq)) <= 1)


s = np.random.uniform(0,1,1)
print('S: {}'.format(s))

if s > 0.5:
    print('amk')
    print(s)