#!/usr/bin/env python
import rospy
import std_msgs
import time

def talker():
    pub = rospy.Publisher('Braking', std_msgs.msg.Bool, queue_size=10)
    #pub2 = rospy.Publisher('Speed', std_msgs.msg.Float32, queue_size=10)    
    rospy.init_node('braking_test')
    #pub2.publish(0)
    pub.publish(True)
    #time.sleep(2)

talker()
