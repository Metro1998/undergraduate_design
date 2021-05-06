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


def get_veh_position(vehID_list):
    vehicle = []
    vehicles_direction = []
    res = []
    for i in vehID_list:
        for j in i:
            traci.vehicle.subscribe(str(j), (tc.VAR_POSITION, ))
            for k in traci.vehicle.getSubscriptionResults(str(j)).values():
            # Only one loop, but transform tuple to the list
                vehicle = list(k)
                print(vehicle)
            vehicles_direction.append(vehicle)
        res.append(vehicles_direction)
    return res
