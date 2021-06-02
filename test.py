import numpy as np
import traci
import traci.constants as tc
import para_dict

"""

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
"""


def rank(lt: list, index: int):
    n = len(lt)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if lt[j][index] > lt[j + 1][index]:
                lt[j], lt[j + 1] = lt[j + 1], lt[j]
    return lt


lt = [[3], [5], [2], [1], [8], [4]]
a = rank(lt=lt, index=0)
a.reverse()
blame = 0.5


def get_border_for_blame(retrospective_length: float, u_section_anchor: list):
    # u_section_anchor is a list [[,],[,],[,],[,]] storing the anchor position of the u_section
    # from north to west respectively

    # now from north to west, left to right, down to up
    north_1 = [u_section_anchor[0][0], u_section_anchor[0][0] + 3.75,
               u_section_anchor[0][1], u_section_anchor[0][1] + retrospective_length]
    north_2 = [u_section_anchor[0][0] + 3.75, u_section_anchor[0][0] + 7.50,
               u_section_anchor[0][1], u_section_anchor[0][1] + retrospective_length]
    east_1 = [u_section_anchor[1][0], u_section_anchor[1][0] + retrospective_length,
              u_section_anchor[1][1] + 3.75, u_section_anchor[1][1] + 7.5]
    east_2 = [u_section_anchor[1][0], u_section_anchor[1][0] + retrospective_length,
              u_section_anchor[1][1], u_section_anchor[1][1] + 3.75]
    south_1 = [u_section_anchor[2][0], u_section_anchor[2][0] + 3.75,
               u_section_anchor[2][1] - retrospective_length, u_section_anchor[2][1]]
    south_2 = [u_section_anchor[2][0] + 3.75, u_section_anchor[2][0] + 7.5,
               u_section_anchor[2][1] - retrospective_length, u_section_anchor[2][1]]
    west_1 = [u_section_anchor[3][0] - retrospective_length, u_section_anchor[3][0],
              u_section_anchor[3][1], u_section_anchor[3][1] + 3.75]
    west_2 = [u_section_anchor[3][0] - retrospective_length, u_section_anchor[3][0],
              u_section_anchor[3][1] + 3.75, u_section_anchor[3][1] + 7.5]
    border_for_blame = [north_1, north_2, east_1, east_2, south_1, south_2, west_1, west_2]
    return border_for_blame


border_for_blame = get_border_for_blame(retrospective_length=196, u_section_anchor=para_dict.u_section_anchor)

veh_position_type = [[[240.63, 288.75919178607387, 0], [240.63, 281.25899661880476, 0], [240.63, 273.7588918503564, 0],
                      [240.63, 266.2587286493064, 0], [244.38, 273.7592210456443, 1], [244.38, 266.2590397474642, 1],
                      [248.13, 288.75546300530584, 2], [248.13, 281.25539387330144, 2], [248.13, 273.7553159675772, 2],
                      [248.13, 266.2551832362574, 2]],
                     [[270.87031381204145, 259.38, 0], [291.8512111919959, 255.63, 1], [288.5489348837335, 251.88, 2],
                      [280.6779030550299, 250.9055, 2], [280.67727703167577, 253.63, 2],
                      [272.9894648054315, 250.9055, 2],
                      [272.98922233352255, 253.63, 2], [265.40105232434087, 251.88, 2]],
                     [[259.38, 233.2582896911518, 0], [255.63, 211.24272352892476, 1], [255.63, 218.74287466811776, 1],
                      [255.63, 226.24303351483496, 1], [255.63, 233.74314898442316, 1], [251.88, 218.74353530701586, 2],
                      [251.88, 226.2436268772998, 2], [251.88, 233.74380030049537, 2]],
                     [[225.49134688756962, 240.63, 0], [204.64271263111942, 248.13, 2], [212.14280398156356, 248.13, 2],
                      [219.64289047706708, 248.13, 2], [227.14305847055914, 248.13, 2], [234.6431917111983, 248.13, 2]],
                     [[240.62, 486.6645448481709, 0], [240.62, 414.36790507890254, 0], [242.62, 458.44380255844163, 1],
                      [244.37, 325.9057168004472, 1], [244.37, 318.3994352795752, 1], [244.37, 310.8972002882855, 1]],
                     [[488.1720744575729, 259.38, 0], [464.07915583197905, 259.38, 0], [417.93553347108923, 259.38, 0],
                      [367.99465508045176, 259.38, 0], [327.4801495977363, 259.38, 0], [371.84593715569633, 255.63, 2],
                      [359.90313100392916, 255.63, 1], [350.1974307046992, 255.63, 1], [340.8605125546697, 255.63, 1],
                      [333.17269035134007, 255.63, 2], [324.6422531162039, 255.63, 2], [314.97068117696006, 255.63, 1]],
                     [[258.38, 14.089872743370377, 1], [255.63, 174.0890378707347, 2], [255.63, 181.5975594667251, 1],
                      [255.63, 189.101102815056, 2]],
                     [[67.81448677125375, 240.62, 0], [21.76463944310003, 243.62, 1], [69.10119584424334, 244.37, 1],
                      [76.89557071368705, 244.37, 2], [84.7584436840338, 244.37, 2], [92.77778645410069, 244.37, 1],
                      [100.28834352553294, 244.37, 2], [108.03188183485233, 244.37, 1], [115.54247521478511, 244.37, 1],
                      [123.16430362889193, 244.37, 2], [130.66841053478583, 244.37, 2], [138.21280192642536, 244.37, 2],
                      [145.71455254842007, 244.37, 1], [153.22841327011955, 244.37, 1], [160.73074030164733, 244.37, 2],
                      [168.23279281113804, 244.37, 2], [175.73407766906308, 244.37, 2], [183.23422588223002, 244.37, 1],
                      [190.73435448337816, 244.37, 1]]]
relative_demand = [0 for x in range(0, 8)]

# -----border for blame-----
# border_for_blame = self.get_border_for_blame(self.retrospective_length, self.u_section_anchor)

# ----blame space----
space_for_blame = []

# we use index to indicate the direction
index = 0
for i in veh_position_type[4:8]:
    space_for_blame_lane1 = []
    space_for_blame_lane2 = []
    # now we enter the loop of each vehicle in the u section
    for _ in i:

        if border_for_blame[index * 2][0] < _[0] < border_for_blame[index * 2][1] and \
                border_for_blame[index * 2][2] < _[1] < border_for_blame[index * 2][3]:
            space_for_blame_lane1.append(_)
        elif border_for_blame[index * 2 + 1][0] < _[0] < border_for_blame[index * 2 + 1][1] and \
                border_for_blame[index * 2 + 1][2] < _[1] < border_for_blame[index * 2 + 1][3]:
            space_for_blame_lane2.append(_)
    space_for_blame.append(space_for_blame_lane1)
    space_for_blame.append(space_for_blame_lane2)
    index += 1
index = 0
for i in space_for_blame:
    if index == 0 or index == 1 or index == 4 or index == 5:
        rank(lt=i, index=1)
    else:
        rank(lt=i, index=0)
    index += 1

index = 0
for i in space_for_blame:
    if index == 0 or index == 1 or index == 2 or index == 3:
        pass
    else:
        i.reverse()
    index += 1

space_for_blame_ = []
for i in space_for_blame:
    space_for_blame_lane_ = []
    for _ in i:
        space_for_blame_lane_.append(_[2])
    space_for_blame_.append(space_for_blame_lane_)
print(space_for_blame_)

lane_index = 0
conut_left = []
count_through = []
for _ in space_for_blame_:
    conut_left_for_lane = 0
    count_through_for_lane = 0
    _.reverse()
    index = []
    for i in range(len(_) - 1):
        if _[i] != _[i + 1]:
            index.append(i)
    index.append(i + 1)
    demand_for_lane = list(1 for x in range(len(_)))
    for j in range(len(index) - 1):
        for m in range(index[j] + 1):
            demand_for_lane[m] *= (1 - blame)
        for m in range(index[j] + 1, index[j + 1] + 1):
            demand_for_lane[m] += blame * (index[j] + 1) / (index[j + 1] - index[j])
    demand_for_lane.reverse()
    print(demand_for_lane)
    _.reverse()

    ix = 0
    for x in _:
        if x == 2:
            conut_left_for_lane += demand_for_lane[ix]
        elif x == 1:
            count_through_for_lane += demand_for_lane[ix]
        ix += 1
    conut_left.append(conut_left_for_lane)
    count_through.append(count_through_for_lane)
    print(conut_left_for_lane)
    print(" ")
for i in range(8):
    if i % 2 == 0:
        relative_demand[i] = conut_left[i] + conut_left[i + 1]
    else:
        relative_demand[i] = count_through[i - 1] + count_through[i]
print(relative_demand)
