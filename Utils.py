# @author  Wolfie
# @date    2021-05-03

import traci
import traci.constants as tc

def get_vehID(edgeID_list):
    res = []
    for i in edgeID_list:
        traci.edge.subscribe(i, (tc.LAST_STEP_VEHICLE_ID_LIST,))
        for j in traci.edge.getSubscriptionResults(i).values():
            res.append(list(j))
    return res


def get_veh_position_type(vehID_list):
    tem = []
    vehicle = []
    vehicles_direction = []
    res = []
    indicator = 0 # Control the vehicle
    for i in vehID_list:
        for j in i:
            traci.vehicle.subscribe(str(j), (tc.VAR_POSITION, tc.VAR_TYPE))
            for k in traci.vehicle.getSubscriptionResults(str(j)).values():
            # Only one loop, but transform tuple to the list
                tem = list(k)
                if len(tem) == 2:
                    vehicle.append(tem[0])
                    vehicle.append(tem[1])
                if len(tem) == 14:
                    vehicle.append(0)
                    indicator = 1
                if len(tem) == 15:
                    vehicle.append(2)
                    indicator = 1
                if len(tem) == 17:
                    vehicle.append(1)
                    indicator = 1
                if indicator == 1:
                    vehicles_direction.append(vehicle)
                    vehicle = []
                    indicator = 0
        res.append(vehicles_direction)
    return res

"""
def get_veh_type(vehID_list):
    vehicle = []
    tem = []
    vehicles_direction = []
    res = []
    for i in vehID_list:
        for j in i:
            traci.vehicle.subscribe(str(j), (tc.VAR_TYPE,))
            for k in traci.vehicle.getSubscriptionResults(str(j)).values():
                # Only one loop, but transform tuple to the list
                vehicle = list(k)
                print(vehicle)
                if len(vehicle) == 14:
                    tem = [0]
                if len(vehicle) == 15:
                    tem = [2]
                else:
                    tem = [1]
            vehicles_direction.append(tem)
        res.append(vehicles_direction)
    return res

"""
