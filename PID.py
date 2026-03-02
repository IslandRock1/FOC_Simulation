
class PID:
    def __init__(self, Kp, Ki, Kd):
        self._Kp = Kp
        self._Ki = Ki
        self._Kd = Kd

        self._integralSum = 0.0
        self._prevError = 0.0

    def update(self, error, dt: float = 1.0):
        self._integralSum += error * dt
        dError = (error - self._prevError) / dt
        out = self._Kp * error + self._Ki * self._integralSum + self._Kd * dError

        self._prevError = error
        return out