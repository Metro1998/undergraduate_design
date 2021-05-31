import numpy as np

blame = 0.5
b = [1, 2, 3, 4]
print(b[0:2])



a = [1, 2, 1, 3, 3, 2, 2, 1, 1]
a.reverse()
index = []
for i in range(len(a)-1):
    if a[i] != a[i + 1]:
        index.append(i)
index.append(i+1)
demand_for_lane = list(1 for x in range(len(a)))
for j in range(len(index)-1):
    for m in range(index[j]+1):
        demand_for_lane[m] *= (1-blame)
    for m in range(index[j]+1, index[j+1]+1):
        demand_for_lane[m] += blame*(index[j]+1)/(index[j+1]-index[j])
demand_for_lane.reverse()
print(demand_for_lane)


