
class PI_Reg:
    def __init__(self, Kp, Ki, *, maxOut=None):
        self._Kp = Kp
        self._Ki = Ki

        self._sum = 0
        self._maxOut = maxOut

    def update(self, error):

        if (self._maxOut is not None) and (abs(self._Kp * error) < self._maxOut):
            self._sum += error

            out = self._Kp * error + self._Ki * self._sum
            return max(-self._maxOut, min(self._maxOut, out))
        return self._Kp * error + self._Ki * self._sum