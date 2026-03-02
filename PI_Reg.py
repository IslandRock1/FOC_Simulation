
class PI_Reg:
    def __init__(self, Kp, Ki):
        self._Kp = Kp
        self._Ki = Ki

        self._sum = 0
        self._setpoint = 0

    def setSetpoint(self, setpoint):
        self._setpoint = setpoint

    def update(self, value):
        error = value - self._setpoint
        self._sum += error

        return self._Kp * error + self._Ki * self._sum