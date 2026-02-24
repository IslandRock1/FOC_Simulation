
import math
from Interface import Interface

class Motor:
    def __init__(self, dt):
        self._simtime = 0.0
        self._dt = dt

        self._T = 0.0
        self._I = 0.0
        self._W = 0.0
        self._theta = 0.0

        self._wOut = 0.0

        self._R = 0.2
        self._L = 0.001
        self._Ke = 0.1
        self._Kt = 0.1
        self._J = 0.0005
        self._B = 0.001

        self._torqueSequenceIx = 0
        self._torqueSequence = [(0.0, 0.0)] # List of sequences, (voltage, angle)

    def _updateCurrent(self, V):
        self._I += (V - self._Ke * abs(self._W) - self._R * self._I) * self._dt / self._L

    def _updateTorque(self, torqueAngle):
        beta = (torqueAngle - self._theta + math.pi) % (2 * math.pi) - math.pi
        self._T = self._Kt * self._I * math.sin(beta)

    def _updateMotor(self):
        # Ignoring external load.
        self._W += (self._T - self._B * self._W) * self._dt / self._J
        self._theta += self._W * self._dt

    def update(self):

        V, torqueAngle = self._torqueSequence[self._torqueSequenceIx]
        self._torqueSequenceIx = (self._torqueSequenceIx + 1) % len(self._torqueSequence)

        self._updateCurrent(V)
        self._updateTorque(torqueAngle)
        self._updateMotor()

        self._simtime += self._dt

    def setTorqueSequence(self, torqueSequence):
        self._torqueSequence = torqueSequence

    def getSimtime(self):
        return self._simtime

    def getTorque(self):
        return self._T

    def getCurrent(self):
        return self._I

    def getVelocity(self):
        return self._W

    def getAngle(self):
        return self._theta

    def getInterface(self) -> Interface:
        i = Interface()
        i.angleMotor = self.getAngle()
        i.angularVelocity = self.getVelocity()
        i.simtime = self.getSimtime()
        i.angleTorque = self.getTorque()
        i.dt = self._dt
        return i