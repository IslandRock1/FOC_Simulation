
import math
from Interface import Interface

class Motor:
    def __init__(self, polePairs, dt):
        self._simtime = 0.0
        self._dt = dt
        self._polePairs = polePairs
        self._V = (0.0, 0.0, 0.0)

        self._Ia = 0.0
        self._Ib = 0.0
        self._Ic = 0.0

        self._T = 0.0                  # Torque (Proportional with acceleration)
        self._W = 0.0                  # Velocity
        self._theta = 0.0              # Angle
        self._thetaElectrical = 0.0    # Electrical angle (polePairs * angle)

        self._wOut = 0.0

        self._R = 0.2
        self._L = 0.001
        self._Ke = 0.1
        self._Kt = 0.1
        self._J = 0.0005
        self._B = 0.001

    def _getBackEMF(self):
        e_a = self._Ke * self._W * math.sin(self._thetaElectrical)
        e_b = self._Ke * self._W * math.sin(self._thetaElectrical - (2 * math.pi / 3.0))
        e_c = self._Ke * self._W * math.sin(self._thetaElectrical + (2 * math.pi / 3.0))
        return (e_a, e_b, e_c)

    def _updateCurrent(self):

        Va, Vb, Vc = self._V
        e_a, e_b, e_c = self._getBackEMF()

        self._Ia += self._dt * (Va - self._R * self._Ia - e_a) / self._L
        self._Ib += self._dt * (Vb - self._R * self._Ib - e_b) / self._L
        self._Ic += self._dt * (Vc - self._R * self._Ic - e_c) / self._L

        if (abs(self._Ia + self._Ib + self._Ic) > 1e-5):
            print(f"Invalid current?")
            print(f"Currents: {self._Ia}, {self._Ib}, {self._Ic} | Sum: {self._Ia + self._Ib + self._Ic}")


    def _updateTorque(self):
        self._T = self._Kt * (
            self._Ia * math.sin(self._thetaElectrical) +
            self._Ib * math.sin(self._thetaElectrical - (2 * math.pi / 3.0)) +
            self._Ic * math.sin(self._thetaElectrical + (2 * math.pi / 3.0))
        )

    def _updateMotor(self):
        # Ignoring external load.
        self._W += (self._T - self._B * self._W) * self._dt / self._J
        self._theta += self._W * self._dt
        self._thetaElectrical = self._polePairs * self._theta

    def setVoltage(self, V):
        Va, Vb, Vc = V
        if abs(Va + Vb + Vc) > 1e-5:
            raise ValueError("Voltage sum must be 0.")

        self._V = V

    def update(self):
        self._updateCurrent()
        self._updateTorque()
        self._updateMotor()

        self._simtime += self._dt

    def getSimtime(self):
        return self._simtime

    def getTorque(self):
        return self._T

    def getCurrent(self):
        return (self._Ia, self._Ib, self._Ic)

    def getVoltage(self):
        return self._V

    def getElectricalPower(self):
        va, vb, vc = self._V
        return va * self._Ia + vb * self._Ib + vc * self._Ic

    def getVelocity(self):
        return self._W

    def getMechanicalPower(self):
        return self._T * self._W

    def getAngle(self):
        return self._theta

    def getElectricalAngle(self):
        return self._thetaElectrical