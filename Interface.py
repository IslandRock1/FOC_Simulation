
class Interface:
    def __init__(self):
        self.simtime = None
        self.dt = None

        self.angleSetpoint = None
        self.angleMotor = None
        self.angularVelocitySetpoint = None
        self.angularVelocity = None
        self.torqueSetpoint = None
        self.forceTorque = None

        self.electricalPower = None
        self.mechanicalPower = None