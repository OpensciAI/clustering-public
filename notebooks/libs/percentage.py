# Find the percentages.

import sys
import numpy as np

args = sys.argv
if len(args) < 3:
    print('pecentage <total> <val1> ... [valn]')
    exit(0)
    
total = np.array(args[1], dtype='int64')
vals = args[2:]
vals = np.array(vals, dtype='int64')
percentages = vals*100.0/total
per_sum = np.sum(percentages)

print(percentages)
print('remaining {}'.format(100-per_sum))