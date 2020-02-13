#!/usr/bin/env python
import motor
import time
import rospy
import std_msgs

#assign static ips for steering/braking nodes
#add try statements to detect e-stop and wait to reconnect

def reset_motor_pos():  #pushes braking all the way to end to recalibrate
    brakingMotor.setDirectDrive(-1400)
    time.sleep(7)

def calibrate_motor():
    brakingMotor.setDirectDrive(-1400)
    time.sleep(6)
    brakingMotor.setDirectDrive(1400)
    time.sleep(1)
    brakingMotor.setDirectDrive(0)
    print("calibrated")         #used for debugging, remove afterwards

def init_motor():
    global brakingMotor
    
    brakingMotor = motor.nextEng("10.5.5.69", 9)
    brakingMotor.connect()
    brakingMotor.setControlMode(3)
    brakingMotor.setCurrentLimit(4000)

def callback(data):                     #should be tested while car is driving, 
    brakes_on = data.data               #to see if current draw can be used as measure of braking power
    if(brakes_on):
        print(speed_pub)
        rospy.Rate(10)
        speed_pub.publish(0)                #turn off speed
        brakingMotor.setDirectDrive(-1400)
        time.sleep(2)                       #turn braking on for 2 secs
        brakingMotor.setDirectDrive(1400)
        time.sleep(1)                       #reverse motor position to unbraked state, possibly play around with value
        brakingMotor.setDirectDrive(0)

def listener():
    rospy.Subscriber('Braking', std_msgs.msg.Bool, callback)
    global speed_pub
    speed_pub = rospy.Publisher('Speed', std_msgs.msg.Float32, queue_size=10)
    rospy.spin()

def main():
    rospy.init_node('braking_node', anonymous=True)
    while(True):                    #used for reconnecting if e-stop is engaged
        try:
            init_motor()
            calibrate_motor()

            listener()

        except:
            pass

if __name__ == "__main__":
    main()
