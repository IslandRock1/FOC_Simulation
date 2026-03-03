from utils.PID import PID
from utils.Interface import Interface
from Visualizer import Visualizer
from Motor import Motor
from Controller import Controller

def main():

    numMagnets = 6
    dt = 0.000001 # 1us
    motor = Motor(numMagnets, dt)
    visu = Visualizer(numMagnets)
    controller = Controller(numMagnets)

    positionSetpoint = 3.1415926 * 2.0
    velocitySetpoint = 0.0

    i = Interface()
    i.simtime = 0.0
    i.dt = dt
    i.angleMotor = motor.getAngle()
    i.angleSetpoint = positionSetpoint
    i.angularVelocity = motor.getVelocity()
    i.angularVelocitySetpoint = velocitySetpoint
    i.forceTorque = motor.getTorque()
    i.torqueSetpoint = 0
    i.totalElectricPower = motor.getTotalElectricPower()
    i.electricalPower = motor.getElectricalPower()
    i.mechanicalPower = motor.getMechanicalPower()

    positionPID = PID(100.0, 0.0, 0.0)
    positionPID.setMax(200.0) # Observed max speed of about 145
    velocityPID = PID(100.0, 0.01, 0.0)
    velocityPID.setMax(1000.0) # Mostly just a guess.

    for _ in range(500):
        visu.update(i)
    print("Simulation started.")

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

            i.totalElectricPower = motor.getTotalElectricPower()
            i.electricalPower = motor.getElectricalPower()
            i.mechanicalPower = motor.getMechanicalPower()

        # 100kHz => every 10'000 nanosecond. Every 10 microseconds.
        if (nanosecond % 10_000 == 0):
            angle = motor.getAngle()
            electricAngle = motor.getElectricalAngle()
            velocity = motor.getVelocity()
            current = motor.getCurrent()

            velocitySetpoint = positionPID.update(positionSetpoint - angle)
            iqRef = velocityPID.update(velocity - velocitySetpoint)
            i.angularVelocitySetpoint = velocitySetpoint

            voltages = controller.getVoltages(iqRef, electricAngle, velocity, current[0], current[1])
            motor.setVoltage(voltages)


        # Just find a number that works.
        # Originally tried 100Hz, (100 FPS).
        # This worked, but seems very choppy
        # as the motor moves very far in the 10ms
        # between frames.
        if (nanosecond % 100_000 == 0):
            b = visu.update(i)
            if (not b): break

            elPower = motor.getElectricalPower()
            mechPower = motor.getMechanicalPower()
            # print(f"Electrical Power: {elPower:.2f}W | Mechanical Power: {mechPower:.2f}W")

    print(f"Simulation finished. Total simulation time: {nanosecond / (1000.0 * 1000.0)} ms.")

if __name__ == "__main__":
    main()
