# @author  Wolfie
# @date    2021-05-03

import traci
import traci.constants as tc
import para_dict
import numpy as np
import math
import torch
import random
import matplotlib.pyplot as plt


# env relative
def generate_routefile():
    random.seed(123)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    pEN = 1. / 17
    pEW = 1. / 19
    pES = 1. / 15
    pNW = 1. / 13
    pNS = 1. / 10
    pNE = 1. / 15
    pWS = 1. / 12
    pWE = 1. / 15
    pWN = 1. / 15
    pSE = 1. / 18
    pSN = 1. / 17
    pSW = 1. / 12

    with open("Data/Metro_Intersection.rou.xml", "w") as routes:
        print("""<routes>
        <vType vClass="private" sigma="0.5" lcStrategic="1.0" jmIgnoreKeepClearTime="0"\
        id="CAV_left" decel="4.5" color="0,255,0" carFollowModel="IDM" accel="3.0" xmlns:maxSpeed="40.0" xmlns:length="5"/>

        <vType vClass="custom1" sigma="0.5" lcStrategic="1.0" jmIgnoreKeepClearTime="0"\
        id="CAV_through" decel="4.5" color="24,116,205" carFollowModel="IDM" accel="3.0" xmlns:maxSpeed="40.0" xmlns:length="5"/>

        <vType vClass="custom2" sigma="0.5" lcStrategic="1.0" jmIgnoreKeepClearTime="0"\
        id="CAV_right" decel="4.5" color="218,112,214" carFollowModel="IDM" accel="3.0" xmlns:maxSpeed="40.0" xmlns:length="5"/>

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
            if random.uniform(0, 1) < pEN:
                print('    <vehicle id="%i" type="CAV_right" route="EN" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pEW:
                print('    <vehicle id="%i" type="CAV_through" route="EW" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pES:
                print('    <vehicle id="%i" type="CAV_left" route="ES" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pNW:
                print('    <vehicle id="%i" type="CAV_right" route="NW" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pNS:
                print('    <vehicle id="%i" type="CAV_through" route="NS" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pNE:
                print('    <vehicle id="%i" type="CAV_left" route="NE" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pWS:
                print('    <vehicle id="%i" type="CAV_right" route="WS" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pWE:
                print('    <vehicle id="%i" type="CAV_through" route="WE" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pWN:
                print('    <vehicle id="%i" type="CAV_left" route="WN" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pSE:
                print('    <vehicle id="%i" type="CAV_right" route="SE" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pSN:
                print('    <vehicle id="%i" type="CAV_through" route="SN" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pSW:
                print('    <vehicle id="%i" type="CAV_left" route="SW" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
        print("</routes>", file=routes)


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


def plot1(queue_length):
    ax1 = plt.subplot(111)
    ax1.cla()
    ax1.grid()
    ax1.set_title('Evaluation_Avg_Queue_Length_blame=0')
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Avg_Queue_Length')
    ax1.plot(queue_length)
    Runtime = len(queue_length)

    # save
    path = 'pic+0/pic' + 'Evaluation_queue_length' + str(Runtime) + '.jpg'
    if Runtime % 1 == 0:
        plt.savefig(path)
    plt.pause(0.0000001)


def plot2(waiting_time):
    ax1 = plt.subplot(111)
    ax1.cla()
    ax1.grid()
    ax1.set_title('Evaluation_Avg_Accumulated_Waiting_Time_blame=0')
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Avg_Accumulated_Waiting_Time')
    ax1.plot(waiting_time)
    Runtime = len(waiting_time)

    # save
    path = 'pic+0/pic' + 'Evaluation_waiting_time' + str(Runtime) + '.jpg'
    if Runtime % 1 == 0:
        plt.savefig(path)
    plt.pause(0.0000001)


def plot3(alpha):
    ax1 = plt.subplot(111)
    ax1.cla()
    ax1.grid()
    ax1.set_title('Alpha_blame=0')
    ax1.set_xlabel('Episode')
    ax1.set_ylabel('Alpha')
    ax1.plot(alpha)
    Runtime = len(alpha)

    # save
    path = 'pic+0/pic' + 'Alpha' + str(Runtime) + '.jpg'
    if Runtime % 1 == 0:
        plt.savefig(path)
    plt.pause(0.0000001)
