import math
from dataclasses import dataclass

from utils.PID import PID
from Motor import Motor
from Controller import Controller

import pg_widgets as pw

@dataclass
class PIDParams:
    positionKp: float
    positionKi: float
    positionKd: float
    maxPosition: float

    velocityKp: float
    velocityKi: float
    velocityKd: float
    maxVelocity: float

    dRegKp: float
    dRegKi: float
    maxD: float
    qRegKp: float
    qRegKi: float
    maxQ: float

@dataclass
class Results:
    name:            str         = None
    setpoints:       list[float] = None
    positions:       list[float] = None
    RMS:             float       = None
    overshoot:       float       = None
    settlingTime:    float       = None

@dataclass
class GlobalParams:
    polePairs: float = 6.0
    dt: float = 0.000001 # 1 us

def testParams(params: PIDParams, results: Results):
    motor = Motor(GlobalParams.polePairs, GlobalParams.dt)
    controller = Controller(GlobalParams.polePairs,
        dRegKp=params.dRegKp, dRegKi=params.dRegKi,
        qRegKp=params.qRegKp, qRegKi=params.qRegKi,
        maxD=params.maxD, maxQ=params.maxQ
        )

    positionPID = PID(params.positionKp, params.positionKi, params.positionKd, maxOut=params.maxPosition)
    velocityPID = PID(params.velocityKp, params.velocityKi, params.velocityKd, maxOut=params.maxVelocity)

    outPositions = []
    for posSetpoint in results.setpoints:
        angle = motor.getAngle()
        electricAngle = motor.getElectricalAngle()
        velocity = motor.getVelocity()
        current = motor.getCurrent()

        velocitySetpoint = positionPID.update(posSetpoint - angle)
        iqRef = velocityPID.update(velocity - velocitySetpoint)

        voltages = controller.getVoltages(iqRef, electricAngle, velocity, current[0], current[1])
        motor.setVoltage(voltages)

        outPositions.append(angle)
        for _ in range(10): motor.update()

    results.positions = outPositions
    errors = [(set - ang) ** 2 for (set, ang) in zip(results.setpoints, results.positions)]
    results.RMS = math.sqrt(sum(errors) / len(errors))

    return results

def getTestCases(numTimestamps):
    setpoints = [1.0] * numTimestamps
    setpoints[0:1000] = [0] * 1000
    stepResponse = Results("Step Response", setpoints)

    return stepResponse

def main():
    computedVals = [1.0, 0.0, 0.0]
    params = PIDParams(
        positionKp=1.0,
        positionKi=0.0,
        positionKd=0.0,
        maxPosition=None,
        velocityKp=1000.0,
        velocityKi=0.0,
        velocityKd=0.0,
        maxVelocity=None,
        dRegKp=1000.0,
        dRegKi=0.0,
        maxD=None,
        qRegKp=1000.0,
        qRegKi=0.0,
        maxQ=None
    )

    timestamps = [0.01 * x for x in range(10001)]
    stepResponse = getTestCases(len(timestamps))
    stepResponse = testParams(params, stepResponse)

    visu = pw.ControlManager()
    plot = pw.Plot((0.0, 0.2), (1.0, 0.8))

    plot.setXLabel("Time (ms)")
    plot.setYLabel("Position (Rad)")
    plot.setValue(timestamps, stepResponse.positions, 0)
    plot.setValue(timestamps, stepResponse.setpoints, 1)

    text = pw.TextBoxes((0.0, 0.0), (1.0, 0.2), labels=[f"{stepResponse.name}", f"RMS: {stepResponse.RMS}"])

    group = pw.UIGroup((0.0, 0.0), (0.5, 1.0))
    group["text"] = text
    group["plot"] = plot
    visu["plotGroup"] = group

    labels = ["Pos Kp", "Pos Ki", "Pos Kd", "Vel Kp", "Vel Ki", "Vel Kd"]
    lower = [0.0] * len(labels)
    upper = [1000.0, 10000.0, 100000.0, 2.0, 1000.0, 1000.0]
    current = [1.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    tuningSliders = pw.TuningSliders((0.5, 0.0), (0.5, 1.0),
        labels=labels, lower_bounds=lower, upper_bounds=upper, current_values=current)
    visu["tuningSliders"] = tuningSliders

    while visu.isRunning():
        visu.update()

        newVals = visu["tuningSliders"].getValue()
        if (newVals != computedVals):
            params.positionKp = newVals[0]
            params.positionKi = newVals[1]
            params.positionKd = newVals[2]
            params.velocityKp = newVals[3]
            params.velocityKi = newVals[4]
            params.velocityKd = newVals[5]

            stepResponse = testParams(params, stepResponse)
            computedVals = newVals

            visu["plotGroup"]["plot"].setValue(timestamps, stepResponse.positions, 0)
            visu["plotGroup"]["plot"].setValue(timestamps, stepResponse.setpoints, 1)
            visu["plotGroup"]["text"].setText(f"RMS: {stepResponse.RMS}", 1)


    visu.close()

if __name__ == "__main__":
    main()