import traci
import traci.constants as tc
import numpy as np


class Reward_Modeling(object):
    def __init__(self, retrospective_length, u_section_anchor, edge_id):
        self.retrospective_length = retrospective_length
        self.u_section_anchor = u_section_anchor
        self.edge_id = edge_id

    def get_veh_id(self):
        veh_id = []
        for i in self.edge_id:
            traci.edge.subscribe(i, (tc.LAST_STEP_VEHICLE_ID_LIST,))
            for _ in traci.edge.getSubscriptionResults(i).values():
                veh_id.append(_)
        return veh_id

    def get_max_veh_accumulated_waiting_time(self):
        all_accumulated_waiting_time = []
        veh_id = self.get_veh_id()
        for i in veh_id:
            for _ in i:
                all_accumulated_waiting_time.append(traci.vehicle.getAccumulatedWaitingTime(_))
        return max(all_accumulated_waiting_time)

    def get_avg_veh_accumulated_waiting_time(self):
        avg_accumulated_waiting_time = 0
        count = 0
        veh_id = self.get_veh_id()
        for i in veh_id:
            for _ in i:
                avg_accumulated_waiting_time += traci.vehicle.getAccumulatedWaitingTime(_)
                count += 1
        avg_accumulated_waiting_time = avg_accumulated_waiting_time / count
        return avg_accumulated_waiting_time
