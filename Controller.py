
import math

class Controller:
    def __init__(self, numMagnets):
        self._numMagnets = numMagnets
        self._torque = 0.0

        self._setAngles()

    def _setAngles(self):
        self._torqueAngle = []
        for ixAngle in range(6 * self._numMagnets):
            self._torqueAngle.append(ixAngle * math.pi / (self._numMagnets * 3))

    def getTorque(self):
        return self._torque

    def getTorqueSequence(self, motorAngle):
        target = motorAngle - math.pi / 2.0
        bestAngle = 0
        bestDiff = 10.0

        for angle in self._torqueAngle:
            d = (target - angle + math.pi) % math.tau - math.pi
            if d < bestDiff:
                bestDiff = d
                bestAngle = angle

        self._torque = bestAngle
        return [(36.0, bestAngle)]