import traci
import traci.constants as tc
import numpy as np


class Demand_Modeling(object):
    def __init__(self, retrospective_length, u_section_anchor, blame, edge_id):
        self.retrospective_length = retrospective_length
        self.u_section_anchor = u_section_anchor
        self.blame = blame
        self.edge_id = edge_id

    def get_veh_id(self):
        veh_id = []
        for i in self.edge_id:
            traci.edge.subscribe(i, (tc.LAST_STEP_VEHICLE_ID_LIST,))
            for _ in traci.edge.getSubscriptionResults(i).values():
                veh_id.append(_)
        return veh_id

    def get_veh_position_type(self):
        veh_position_type_edges = []
        veh_id = self.get_veh_id()
        for i in veh_id:
            veh_position_type_edge = []
            for j in i:
                vehicle = []
                traci.vehicle.subscribe(j, (tc.VAR_POSITION, tc.VAR_TYPE))
                for _ in traci.vehicle.getSubscriptionResults(j).values():
                    # just loop for twice
                    # eg.
                    # (240.63, 288.7583203267984)
                    # CAV_right
                    if len(_) == 2:
                        # vehicle get the x y position
                        vehicle.append(_[0])
                        vehicle.append(_[1])
                    # we represent right through and left to 0 1 2 respectively
                    if len(_) == 9:
                        vehicle.append(0)
                    if len(_) == 11:
                        vehicle.append(1)
                    if len(_) == 8:
                        vehicle.append(2)
                veh_position_type_edge.append(vehicle)
            veh_position_type_edges.append(veh_position_type_edge)
        return veh_position_type_edges

    def get_absolute_demand(self):
        # absolute_demand is a list of 1 * 8, in which
        # the number of vehicles are stored in north to west and left to through respectively
        absolute_demand = [0 for x in range(0, 8)]
        veh_position_type = self.get_veh_position_type()
        print(veh_position_type)
        # we use index to indicate the direction
        index = 0
        for i in veh_position_type[0:4]:
            # now we enter the loop of each vehicle in the c section
            for _ in i:
                if _[2] == 2:
                    absolute_demand[2 * index] += 1
                if _[2] == 1:
                    absolute_demand[2 * index + 1] += 1
                else:
                    pass
            index += 1
        return absolute_demand

    def get_relative_demand(self):
        # relative_demand is a list of 1 * 8, in which
        # the number of vehicles are stored in north to west and left to through respectively
        relative_demand = [0 for x in range(0, 8)]

        # -----border for blame-----
        border_for_blame = self.get_border_for_blame(self.retrospective_length, self.u_section_anchor)

        # ----blame space----
        space_for_blame = []

        veh_position_type = self.get_veh_position_type()
        # we use index to indicate the direction
        index = 0
        for i in veh_position_type[4:8]:
            if index == 0 or index == 2:
                i.reverse()
            else:
                pass
            space_for_blame_lane1 = []
            space_for_blame_lane2 = []
            # now we enter the loop of each vehicle in the u section
            for _ in i:
                if border_for_blame[index * 2][0] < _[0] < border_for_blame[index * 2][1] and \
                        border_for_blame[index * 2][2] < _[1] < border_for_blame[index][3]:
                    space_for_blame_lane1.append(_[2])
                elif border_for_blame[index * 2 + 1][0] < _[0] < border_for_blame[index * 2 + 1][1] and \
                        border_for_blame[index * 2 + 1][2] < _[1] < border_for_blame[index * 2 + 1][3]:
                    space_for_blame_lane2.append(_[2])
                space_for_blame.append(space_for_blame_lane1)
                space_for_blame.append(space_for_blame_lane2)
            index += 1

        # -----get relative demand-----
        # introduction to "blame"
        # 1.the total demand cant be changed
        # 2.vehicle only blame different vehicle just before itself
        # 3.the process of blame is from end to  start
        # 4.when blaming, the demand which is initialized to 1 will time (1-blame)
        # eg. [2, 0, 1, 1, 2, 0, 0] suppose blame = 0.5
        #     [1, 1, 1, 1, 1, 1, 1]-->[1, 1, 1, 1, 2, 0.5, 0.5]
        # --> [1, 1, 1.75, 1.75, 1, 0.25, 0.25]-->[3.5, 0.875, 0.875, 0.5, 0.125, 0.125]

        # we use lane_index to indicate which lane's demand is countering
        lane_index = 0
        for _ in space_for_blame:
            _.reverse()
            index = []
            for i in range(len(_) - 1):
                if _[i] != _[i + 1]:
                    index.append(i)
            index.append(i + 1)
            demand_for_lane = list(1 for x in range(len(_)))
            for j in range(len(index) - 1):
                for m in range(index[j] + 1):
                    demand_for_lane[m] *= (1 - self.blame)
                for m in range(index[j] + 1, index[j + 1] + 1):
                    demand_for_lane[m] += self.blame * (index[j] + 1) / (index[j + 1] - index[j])

            demand_for_lane.reverse()
            _.reverse()
            count = 0

            for k in _:
                if k == 2:
                    relative_demand[lane_index * 2] += demand_for_lane[count]
                if k == 1:
                    relative_demand[lane_index * 2 + 1] += demand_for_lane[count]
                count += 1
            lane_index += 1
        return relative_demand

    def get_border_for_blame(self, retrospective_length: float, u_section_anchor: list):
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
