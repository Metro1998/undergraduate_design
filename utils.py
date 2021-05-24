# @author  Wolfie
# @date    2021-05-03

import traci
import traci.constants as tc
import Para_dict
import numpy as np
import math
import torch


# env relative
def generate_route(args):
    np.random.seed(args.seed)
    N = 3600  # number of time steps
    # demand per second from different directions
    pNW = args.route[0]
    pNS = args.route[1]
    pNE = args.route[2]
    pEN = args.route[3]
    pEW = args.route[4]
    pES = args.route[5]
    pSE = args.route[6]
    pSN = args.route[7]
    pSW = args.route[8]
    pWS = args.route[9]
    pWE = args.route[10]
    pWN = args.route[11]

    with open("Data/Metro_Intersection.rou.xml", "w") as routes:
        routes.truncate()
        print("""<routes>
            <vType id="passenger_left" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
    guiShape="passenger"/>
            <vType id="passenger_through" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
    guiShape="passenger"/>
            <vType id="passenger_right" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
    guiShape="passenger"/>
            <vType id="bus_left" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>
            <vType id="bus_through" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>
            <vType id="bus_right" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>
            <route id="EN" edges="east_u east_c north_out" />
            <route id="EW" edges="east_u east_c west_out" />
            <route id="ES" edges="east_u east_c south_out" />
            <route id="NW" edges="north_u north_c west_out" />
            <route id="NS" edges="north_u north_c south_out" />
            <route id="NE" edges="north_u north_c east_out" />
            <route id="WS" edges="west_u west_c south_out" />
            <route id="WE" edges="west_u west_c east_out" />
            <route id="WN" edges="west_u west_c north_out" />
            <route id="SE" edges="south_u south_c east_out" />
            <route id="SN" edges="south_u south_c north_out" />
            <route id="SW" edges="south_u south_c west_out" />
            """, file=routes)
        vehNr = 0
        for i in range(N):
            if np.random.uniform(0, 1) < pEN:
                print('    <vehicle id="%i" type="passenger_right" route="EN" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if np.random.uniform(0, 1) < pEW:
                print('    <vehicle id="%i" type="passenger_through" route="EW" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if np.random.uniform(0, 1) < pES:
                print('    <vehicle id="%i" type="passenger_left" route="ES" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if np.random.uniform(0, 1) < pNW:
                print('    <vehicle id="%i" type="passenger_right" route="NW" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if np.random.uniform(0, 1) < pNS:
                print('    <vehicle id="%i" type="passenger_through" route="NS" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if np.random.uniform(0, 1) < pNE:
                print('    <vehicle id="%i" type="passenger_left" route="NE" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if np.random.uniform(0, 1) < pWS:
                print('    <vehicle id="%i" type="passenger_right" route="WS" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if np.random.uniform(0, 1) < pWE:
                print('    <vehicle id="%i" type="passenger_through" route="WE" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if np.random.uniform(0, 1) < pWN:
                print('    <vehicle id="%i" type="passenger_left" route="WN" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if np.random.uniform(0, 1) < pSE:
                print('    <vehicle id="%i" type="passenger_right" route="SE" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if np.random.uniform(0, 1) < pSN:
                print('    <vehicle id="%i" type="passenger_through" route="SN" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if np.random.uniform(0, 1) < pSW:
                print('    <vehicle id="%i" type="passenger_left" route="SW" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
        print("</routes>", file=routes)


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
    indicator = 0  # Control the vehicle
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
                    vehicle.append(1)
                    indicator = 1
                if len(tem) == 15:
                    vehicle.append(3)
                    indicator = 1
                if len(tem) == 17:
                    vehicle.append(2)
                    indicator = 1
                if indicator == 1:
                    vehicles_direction.append(vehicle)
                    vehicle = []
                    indicator = 0
        res.append(vehicles_direction)
        vehicles_direction = []
    return res


def chessboard(vehicle_position_type):
    column_index = 0
    row_index = 0
    m_east = np.zeros((3, 54))
    m_north = np.zeros((3, 54))
    m_west = np.zeros((3, 54))
    m_south = np.zeros((3, 54))
    m = []
    for i in range(0, 8, 1):
        for j in vehicle_position_type[i]:
            # In one direction, each vehicle
            if i == 0 or i == 4:
                # The direction of east
                row_index = (j[1] - Para_dict.anchor_list_updated[0][2]) // 3.5
                column_index = (j[0] - Para_dict.anchor_list_updated[0][0]) // 7.5
                m_east[int(row_index)][int(column_index)] = j[2]
            if i == 1 or i == 5:
                row_index = (Para_dict.anchor_list_updated[1][3] - j[0]) // 3.5
                column_index = (j[1] - Para_dict.anchor_list_updated[1][0]) // 7.5
                m_north[int(row_index)][int(column_index)] = j[2]
            if i == 2 or i == 6:
                row_index = (Para_dict.anchor_list_updated[2][3] - j[1]) // 3.5
                column_index = (Para_dict.anchor_list_updated[2][1] - j[0]) // 7.5
                m_west[int(row_index)][int(column_index)] = j[2]
            if i == 3 or i == 7:
                row_index = (j[0] - Para_dict.anchor_list_updated[3][2]) // 3.5
                column_index = (Para_dict.anchor_list_updated[3][1] - j[1]) // 7.5
                m_south[int(row_index)][int(column_index)] = j[2]
    m = np.stack((m_east, m_north, m_west, m_south))
    return m


def create_log_gaussian(mean, log_std, t):
    quadratic = -((0.5 * (t - mean) / (log_std.exp())).pow(2))
    l = mean.shape
    log_z = log_std
    z = l[-1] * math.log(2 * math.pi)
    log_p = quadratic.sum(dim=-1) - log_z.sum(dim=-1) - 0.5 * z
    return log_p


def logsumexp(inputs, dim=None, keepdim=False):
    if dim is None:
        inputs = inputs.view(-1)
        dim = 0
    s, _ = torch.max(inputs, dim=dim, keepdim=True)
    outputs = s + (inputs - s).exp().sum(dim=dim, keepdim=True).log()
    if not keepdim:
        outputs = outputs.squeeze(dim)
    return outputs


def soft_update(target, source, tau):
    for target_param, param in zip(target.parameters(), source.parameters()):
        target_param.data.copy_(target_param.data * (1.0 - tau) + param.data * tau)


def hard_update(target, source):
    for target_param, param in zip(target.parameters(), source.parameters()):
        target_param.data.copy_(param.data)
