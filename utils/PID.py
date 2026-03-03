
class PID:
    def __init__(self, Kp, Ki, Kd, *, maxOut=None):
        self._Kp = Kp
        self._Ki = Ki
        self._Kd = Kd

        self._maxOut = maxOut
        self._integralSum = 0.0
        self._prevError = 0.0

    def setMax(self, value):
        self._maxOut = value

    def update(self, error, dt: float = 1.0):

        if (self._maxOut is not None) and (abs(error * self._Kp) < self._maxOut):
            self._integralSum += error * dt

        dError = (error - self._prevError) / dt
        out = self._Kp * error + self._Ki * self._integralSum + self._Kd * dError
        self._prevError = error

        if (self._maxOut is not None):
            return max(-self._maxOut, min(self._maxOut, out))
        return out