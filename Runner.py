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
import Para_dict

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
    pES = 1./ 23
    pNW = 1./ 24
    pNS = 1./ 25
    pNE = 1./ 17
    pWS = 1./ 18
    pWE = 1./ 19
    pWN = 1./ 20
    pSE = 1./ 21
    pSN = 1./ 17
    pSW = 1./ 15

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
            if random.uniform(0, 1) < pEN:
                print('    <vehicle id="%i" type="passenger_right" route="EN" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pEW:
                print('    <vehicle id="%i" type="passenger_through" route="EW" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pES:
                print('    <vehicle id="%i" type="passenger_left" route="ES" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pNW:
                print('    <vehicle id="%i" type="passenger_right" route="NW" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pNS:
                print('    <vehicle id="%i" type="passenger_through" route="NS" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pNE:
                print('    <vehicle id="%i" type="passenger_left" route="NE" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pWS:
                print('    <vehicle id="%i" type="passenger_right" route="WS" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pWE:
                print('    <vehicle id="%i" type="passenger_through" route="WE" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pWN:
                print('    <vehicle id="%i" type="passenger_left" route="WN" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pSE:
                print('    <vehicle id="%i" type="passenger_right" route="SE" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pSN:
                print('    <vehicle id="%i" type="passenger_through" route="SN" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pSW:
                print('    <vehicle id="%i" type="passenger_left" route="SW" depart="%i" />' % (
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
        vehID = utils.get_vehID(Para_dict.edgeID_list)
        vehicle_position_type = utils.get_veh_position_type(vehID)
        chess = utils.chessboard(vehicle_position_type)
        print(chess)
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
