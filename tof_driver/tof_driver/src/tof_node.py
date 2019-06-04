#!/usr/bin/env python
import smbus
import time
import sys
import os

import rospy

from tof_driver.tof import ToF
from tof_driver.srv import SetToFState, SetToFStateResponse

class ToFHandler(object):
    def __init__(self, sensor_name, mux_port):

        self.sensor_name = sensor_name
        self.mux_port = mux_port

        self.node_name = rospy.get_name()
        self.veh_name = self.node_name.split("/")[1]

        self.current_state = True

        self.state_service = rospy.Service('~set_%s_state'%self.sensor_name,
                           SetToFState,
                           self.state_handler)

        self.sensor = ToF()


    def state_handler(self, req):
        self.current_state = req.state
        return SetToFStateResponse("Success")

    def publish_data(self):
        mux = smbus.SMBus(1)
        mux.write_byte(0x70, self.mux_port)
        time.sleep(0.001)
        sensor = ToF()
        try:
            if sensor.begin() == True:
                try:
                    distance = sensor.takeMeasurement()[0]
                    print 'Distance of sensor %s'%self.sensor_name
                    print distance
                except:
                    print 'Could not take Measurement for %s'%self.sensor_name
            else:
                print 'Could not enable %s'%self.sensor_name
        except:
            print 'error'

        #
        #
        #
        #
        #
        # fp = smbus.SMBus(1)
        # fp.write_byte(0x70, self.mux_port)
        # time.sleep(0.001)
        # print 'Tesst 1'
        # if self.sensor.begin()==True:
        #     print 'Testtts 2'
        #     try:
        #         distance = sensor1.takeMeasurement()[0]
        #         print 'Wheeiiiii'
        #         #return GetToFDistance.distanceToF1(ToFDistance1)        #?????????
        #     except:
        #         print 'Could not take Measurement for %s'%self.sensor_name
        # else:
        #     print 'Could not enable %s'%self.sensor_name

if __name__ == '__main__':
    rospy.init_node('~tof_node', anonymous=False)

    tof_sensors = {}

    tof_sensors['left'] = ToFHandler('left_tof',4)
    tof_sensors['middle'] = ToFHandler('middle_tof',2)
    tof_sensors['right'] = ToFHandler('right_tof',1)

    while not rospy.is_shutdown():
        for sensor_name,sensor in tof_sensors.iteritems():
            try:
                if sensor.current_state:
                    sensor.publish_data()
            except IOError as (errno, strerror):
                print "I/O error({0}): {1}".format(errno, strerror)

        time.sleep(0.001)
