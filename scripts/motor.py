import socket
import time
import random
import struct
import sys
import threading



class nextEng(object):
    
    def __init__(self, ipAddress, port):
        self.ipAddress = ipAddress
        self.port = port

    def connect(self):        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.sock.settimeout(0.2)
        self.sa = (self.ipAddress, self.port)
        self.sock.connect(self.sa)
    
    def boardTemperature(self):
        pass

    def busVoltage(self):
        pass

    def setLeds(self, red, blue, green):
        self.sendUint(8, red)
        self.sendUint(9, blue)
        self.sendUint(10, green)

    def setWheelDiameter(self, diameter):
        self.sendFloat(53, diameter)

    def getWheelVelocity(self):
        return self.getFloat(34)

    def getVelocity(self):
        return self.getFloat(28)

    def setDirectDrive(self, pwm):
        self.sendFloat(70, pwm)

    def setWheelVelocity(self, velocity):
        self.sendFloat(20, velocity)

    def setAcceleration(self, accel):
        self.sendFloat(25, accel)

    def setDeceleration(self, decel):
        self.sendFloat(26, decel)

    def setCurrentLimit(self, limit):
        self.sendUint(37, limit)

    def currentEncoderTicks(self):
        return self.getInt(52)

    def hallStatus(self):
        return self.getInt(57)
        
    def angularVelocity(self):
        return self.getFloat(33)

    def tickVelocity(self):
        return self.getFloat(31)

    def rpsVelocity(self):
        return self.getFloat(32)

    def setEncoderTicks(self, ticks):
        self.sendUint(60, int(ticks))

    def setControlMode(self, mode):
        self.sendUint(27, mode)

    def setPid(self, prop, integ, diff):
        self.sendFloat(22, prop)
        self.sendFloat(23, integ)
        self.sendFloat(24, diff)

    def requestTickVelocity(self, velocity):
        self.sendFloat(35, velocity)

    def windUpGaurd(self, value):
        self.sendFloat(36, value)

    def sendInt(self, register, value):
        packet = b''
        packet += struct.pack('B', register)
        packet += struct.pack('B', 0)
        packet += struct.pack('l', value)
        self.sendPacket(packet)
        self.recvPacket()

    def sendUint(self, register, value):
        packet = b''
        packet += struct.pack('B', register)
        packet += struct.pack('B', 0)
        packet += struct.pack('L', value)
        self.sendPacket(packet)
        self.recvPacket()

    def sendFloat(self, register, value):
        packet = b''
        packet += struct.pack('B', register)
        packet += struct.pack('B', 0)
        packet += struct.pack('f', value)
        self.sendPacket(packet)
        self.recvPacket()

    def sendDouble(self, register, value):
        packet = b''
        packet += struct.pack('B', register)
        packet += struct.pack('B', 0)
        packet += struct.pack('d', value)
        self.sendPacket(packet)
        self.recvPacket()

    def getInt(self, register):
        packet = b''
        packet += struct.pack('B', register)
        packet += struct.pack('B', 0)
        self.sendPacket(packet)
        return struct.unpack('i', self.recvPacket() )[0]

    def getUint(self, register):
        packet = b''
        packet += struct.pack('B', register)
        packet += struct.pack('B', 0)
        self.sendPacket(packet)
        return struct.unpack('L', self.recvPacket())[0]

    def getFloat(self, register):
        packet = b''
        packet += struct.pack('B', register)
        packet += struct.pack('B', 0)
        self.sendPacket(packet)
        return struct.unpack('f', self.recvPacket())[0]
        
    def getDouble(self, register):
        packet = b''
        packet += struct.pack('B', register)
        packet += struct.pack('B', 0)
        self.sendPacket(packet)
        return struct.unpack('d', self.recvPacket())[0]

    def sendPacket(self, packet):
        self.sock.send(packet)

    def recvPacket(self):
        x = self.sock.recv(100)
        return x

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()

class robotBase(object):

    def __init__(self, motor1, motor2):
        self.motor1 = motor1
        self.motor2 = motor2
        self.newConnect = 0
        pass

    def connectMotors(self):
        try:
            self.motor1.connect()
            self.motor2.connect()
        except:
            print ("reconnecting")
            pass

    
    def disconnectMotors(self):
        try:
            self.motor1.close()
            self.motor2.close()
        except:
            pass


    def initMotors(self):

        self.motor1.setCurrentLimit(2200)
        self.motor1.windUpGaurd(1500)
        self.motor1.setEncoderTicks(735 * 4)
        self.motor1.setControlMode(2)
        self.motor1.setPid(0.05, 0.065, 0.01)
        self.motor1.setWheelDiameter(.4)
        self.motor1.setAcceleration(6)
        self.motor1.setDeceleration(6)

        self.motor2.setCurrentLimit(2200)
        self.motor2.windUpGaurd(1500)
        self.motor2.setEncoderTicks(735 * 4)
        self.motor2.setControlMode(2)
        self.motor2.setPid(0.05, 0.065, 0.01)
        self.motor2.setWheelDiameter(.4)
        self.motor2.setAcceleration(6)
        self.motor2.setDeceleration(6)

        
    def setWheelVel(self, v1, v2):
        try:
            self.motor1.setWheelVelocity(v1)
            self.motor2.setWheelVelocity(v2)
        except:
            pass

    def getEncoderPos(self):
        try:
            pos1 = self.motor1.currentEncoderTicks()
            pos2 = self.motor2.currentEncoderTicks()
            return pos1, pos2
        except:
            return None

    def checkConnected(self):
        try:
            self.motor1.currentEncoderTicks()
            self.motor2.currentEncoderTicks()
            return 1
        except:
            self.disconnectMotors()
            return 0

    def systemCheck(self):

        # if the motor drivers have been disconnected
        if self.checkConnected() == 0:
            print ("EStop")
            while self.checkConnected() == 0:
                self.connectMotors()
                time.sleep(1)
            print ("reinit motors")
            self.initMotors()
        else:
            return 1

        
if __name__ == "__main__":
             
    motor1 = nextEng("192.168.8.116", 9)
    motor1.connect()
    motor1.setCurrentLimit(5000)
    motor1.windUpGaurd(5000)
    motor1.setEncoderTicks(735 * 4)
    motor1.setControlMode(2)
    motor1.setPid(0.35, 0.12, 0.00)
    motor1.setWheelDiameter(.4)
    motor1.setAcceleration(6)
    motor1.setDeceleration(6)

    print(motor1.currentEncoderTicks())
    motor1.requestTickVelocity(-1000)
    #print(motor1.tickVelocity())
    time.sleep(3)
    motor1.requestTickVelocity(1000)
    time.sleep(3)
    motor1.requestTickVelocity(0)
    #motor1.setLeds(1340,0,0)s
        #motor1.setLeds(0,0,0)



