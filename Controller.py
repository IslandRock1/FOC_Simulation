
import math
from PI_Reg import PI_Reg

class Controller:
    def __init__(self, polePairs):

        self._polePairs = polePairs

        self._parkId = 0.0
        self._parkIq = 0.0
        self._parkVd = 0.0
        self._parkVq = 20.0

        self._clarkeIa = 0.0
        self._clarkeIb = 0.0
        self._clarkeVa = 0.0
        self._clarkeVb = 0.0

        self._piregD = PI_Reg(0.1, 0.0)
        self._piregQ = PI_Reg(0.1, 0.0)

        self._V = [0.0, 0.0, 0.0]

    def getVoltages(self, thetaElectrical, angularVelocity, Ia, Ib):

        self._clarkeTransform(Ia, Ib)
        self._parkTransform(thetaElectrical)
        self._PILoop(angularVelocity)
        self._inversePark(thetaElectrical)
        self._inverseClarke()
        self._subtractAvg()

        print(f"Voltages: {self._V}")
        return self._V

    def _clarkeTransform(self, Ia, Ib):
        # Since i_a + i_b + i_c = 0, only need i_a, i_b

        self._clarkeIa = Ia
        self._clarkeIb = (Ia + 2 * Ib) / math.sqrt(3.0)

    def _parkTransform(self, thetaElectrical):
        self._parkId = math.cos(thetaElectrical) * self._clarkeIa + math.sin(thetaElectrical) * self._clarkeIb
        self._parkIq = -math.sin(thetaElectrical) * self._clarkeIa + math.cos(thetaElectrical) * self._clarkeIb

    def _PILoop(self, angularVelocity):
        pass

    def _inversePark(self, thetaElectrical):
        self._clarkeVa = math.cos(thetaElectrical) * self._parkVd - math.sin(thetaElectrical) * self._parkVq
        self._clarkeVb = math.sin(thetaElectrical) * self._parkVd + math.cos(thetaElectrical) * self._parkVq

    def _inverseClarke(self):
        self._V[0] = self._clarkeVa
        self._V[1] = - self._clarkeVa / 2.0 + self._clarkeVb * math.sqrt(3.0) / 2.0
        self._V[2] = - self._clarkeVa / 2.0 - self._clarkeVb * math.sqrt(3.0) / 2.0

    def _subtractAvg(self):
        avg = sum(self._V) / 3.0
        self._V[0] -= avg
        self._V[1] -= avg
        self._V[2] -= avg