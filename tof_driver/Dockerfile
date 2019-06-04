FROM duckietown/rpi-duckiebot-base:master18

RUN [ "cross-build-start" ]

RUN apt-get update

RUN pip install --upgrade pip

RUN apt-get install python-smbus
# RUN apt-get install ros-kinetic-message-generation
RUN apt-get install i2c-tools

#Copy the package
RUN mkdir -p /catkin_ws/src/tof_driver
COPY tof_driver /catkin_ws/src/tof_driver
RUN /bin/bash -c "source /opt/ros/kinetic/setup.bash; cd /catkin_ws; catkin_make"

RUN [ "cross-build-end" ]

CMD /bin/bash -c "source /catkin_ws/devel/setup.bash; rosrun tof_driver tof_node.py" ]


