
class PI_Reg:
    def __init__(self, Kp, Ki):
        self._Kp = Kp
        self._Ki = Ki

        self._sum = 0

    def update(self, error):
        self._sum += error
        return self._Kp * error + self._Ki * self._sum