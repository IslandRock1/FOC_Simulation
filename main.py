
import math
from time import perf_counter

from Interface import Interface
from Visualizer import Visualizer
from Motor import Motor
from Controller import Controller

def main():

    numMagnets = 6
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

    for _ in range(500):
        visu.update(i)
    print("Starting simulation!")

    nanosecond = -1
    while True:
        nanosecond += 1

        # Simulate motor every microsecond.
        if (nanosecond % 1000 == 0):
            motor.update()

            i.simtime = motor.getSimtime()
            i.angleMotor = motor.getAngle()
            i.angularVelocity = motor.getVelocity()
            i.forceTorque = motor.getTorque()

        # 100kHz => every 10'000 nanosecond. Every 10 microseconds.
        if (nanosecond % 10_000 == 0):
            angle = motor.getAngle()
            torqueSequence = controller.getTorqueSequence(angle)
            motor.setTorqueSequence(torqueSequence)

            i.angleTorque = controller.getTorque()


        # Just find a number that works.
        # Originally tried 100Hz, (100 FPS).
        # This worked, but seems very choppy
        # as the motor moves very far in the 10ms
        # between frames.
        if (nanosecond % 40_000 == 0):
            b = visu.update(i)
            if (not b): break

    print(f"Simulation finished. Total simulation time: {nanosecond / (1000 * 1000)} ms.")

if __name__ == "__main__":
    main()
