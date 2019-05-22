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
    	try:
    		fp = smbus.SMBus(1)
    		fp.write_byte(0x70, self.mux_port)
    		time.sleep(0.001)
    		if self.sensor.begin()==True:
    			try:
    				distance = sensor1.takeMeasurement()[0]
    				print '%s distance:'%self.sensor_name,distance
                    #return GetToFDistance.distanceToF1(ToFDistance1)        #?????????
    			except:
    				print 'Could not take Measurement for %s'%self.sensor_name
    		else:
				print 'Could not enable %s'%self.sensor_name
    	except IOError as (errno, strerror):
    		print "I/O error({0}): {1}".format(errno, strerror)



if __name__ == '__main__':
    rospy.init_node('~tof_node', anonymous=False)

    tof_sensors = {}

    tof_sensors['left'] = ToFHandler('left_tof',0x01)
    tof_sensors['middle'] = ToFHandler('middle_tof',0x02)
    tof_sensors['right'] = ToFHandler('right_tof',0x04)

    while not rospy.is_shutdown():
        for sensor_name,sensor in tof_sensors.iteritems():
            if sensor.current_state:
                sensor.publish_data()
        time.sleep(0.001)
