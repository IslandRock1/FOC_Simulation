
import math
from time import perf_counter

from Interface import Interface
from Visualizer import Visualizer
from Motor import Motor
from Controller import Controller

def main():

    numMagnets = 2
    dt = 0.000001 # 1us
    motor = Motor(dt)
    visu = Visualizer(numMagnets)
    controller = Controller(numMagnets)

    i = Interface()
    i.simtime = 0.0
    i.dt = dt
    i.angleMotor = motor.getAngle()
    i.angularVelocity = motor.getVelocity()
    i.angleTorque = controller.getTorque()
    i.forceTorque = motor.getTorque()

    motor.setTorqueSequence([(0.0, 0.0)])

    while visu.update(i):

        for _ in range(10):
            motor.update()
            motor.setTorqueSequence(controller.getTorqueSequence(motor.getAngle()))

        i.simtime = motor.getSimtime()
        i.angleMotor = motor.getAngle()
        i.angularVelocity = motor.getVelocity()
        i.angleTorque = controller.getTorque()
        i.forceTorque = motor.getTorque()

if __name__ == "__main__":
    main()
