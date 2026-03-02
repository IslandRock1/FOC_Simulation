
import math
from time import perf_counter

from Interface import Interface
from Visualizer import Visualizer
from Motor import Motor
from Controller import Controller

def main():

    numMagnets = 6
    dt = 0.000001 # 1us
    motor = Motor(numMagnets, dt)
    visu = Visualizer(numMagnets)
    controller = Controller(numMagnets)

    i = Interface()
    i.simtime = 0.0
    i.dt = dt
    i.angleMotor = motor.getAngle()
    i.angularVelocity = motor.getVelocity()
    i.angleTorque = controller.getTorque()
    i.forceTorque = motor.getTorque()

    motor.setVoltage((0.0, 0.0, 0.0))

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
            motor.setVoltage((-1.0, 2.0, -1.0))


        # Just find a number that works.
        # Originally tried 100Hz, (100 FPS).
        # This worked, but seems very choppy
        # as the motor moves very far in the 10ms
        # between frames.
        if (nanosecond % 40_000 == 0):
            b = visu.update(i)
            if (not b): break

            elPower = motor.getElectricalPower()
            mechPower = motor.getMechanicalPower()
            print(f"Electrical Power: {elPower:.2f}W | Mechanical Power: {mechPower:.2f}W")

    print(f"Simulation finished. Total simulation time: {nanosecond / (1000.0 * 1000.0)} ms.")

if __name__ == "__main__":
    main()
