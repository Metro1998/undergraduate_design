# !/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2021 German Aerospace Center (DLR) and others.
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0/
# This Source Code may also be made available under the following Secondary
# Licenses when the conditions for such availability set forth in the Eclipse
# Public License 2.0 are satisfied: GNU General Public License, version 2
# or later which is available at
# https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later

# @file    runner.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @date    2009-03-26

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import utils
import para_dict

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")



import traci  # noqa
import traci.constants as tc


def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    pEN = 1./ 10
    pEW = 1./ 11
    pES = 1./ 9
    pNW = 1./ 8
    pNS = 1./ 10
    pNE = 1./ 7
    pWS = 1./ 21
    pWE = 1./ 19
    pWN = 1./ 15
    pSE = 1./ 21
    pSN = 1./ 17
    pSW = 1./ 15

    with open("Data/Metro_Intersection.rou.xml", "w") as routes:
        routes.truncate()
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


# The program looks like this
#    <tlLogic id="0" type="static" programID="0" offset="0">
# the locations of the tls are      NESW
#        <phase duration="31" state="GrGr"/>
#        <phase duration="6"  state="yryr"/>
#        <phase duration="31" state="rGrG"/>
#        <phase duration="6"  state="ryry"/>
#    </tlLogic>


def run():
    """execute the TraCI control loop"""
    vehID = []
    step = 0
    # we start with phase 2 where EW has green
    traci.trafficlight.setPhase("SmartMetro", 2)
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehID = utils.get_vehID(para_dict.edgeID_list)
        print(vehID)
        """
           vehicle_position_type = utils.get_veh_position_type(vehID)
        chess = utils.chessboard(vehicle_position_type)
        print(chess)
        """

        if traci.trafficlight.getPhase("SmartMetro") == 2:
            # we are not already switching
            if traci.inductionloop.getLastStepVehicleNumber("D_1") > 0:
                # there is a vehicle from the north, switch
                traci.trafficlight.setPhase("SmartMetro", 3)
            else:
                # otherwise try to keep green for EW
                traci.trafficlight.setPhase("SmartMetro", 2)
        step += 1
    traci.close()
    sys.stdout.flush()

if __name__ == "__main__":
    generate_routefile()
    traci.start(["sumo", "-c", "Data/Metro_Intersection.sumocfg"], label="sim1")
    run()
