
import math
from time import perf_counter
import pygame as pg
import pg_widgets as pw

from Interface import Interface

def getTextAndPos(numMagnets):
    textDist = 0.4
    midX = 0.5
    midY = 0.5

    angle = 0.0
    currentPositions = []
    for i in range(6 * numMagnets):
        currentPositions.append((midX + textDist * math.cos(angle), midY + textDist * math.sin(angle)))
        angle += 2 * math.pi / (6 * numMagnets)
    texts = ["A+", "B+", "C+", "A-", "B-", "C-"] * numMagnets
    return texts, currentPositions

class Visualizer:
    def __init__(self, numMagnets):
        self._controlManager = pw.ControlManager()

        self._t0 = perf_counter()
        self._numMagnets = numMagnets
        self.setup()

    def setup(self):
        x, y = self._controlManager.getSize()
        w, h = 500, 500
        self._controlManager["freeDraw"] = pw.FreeDraw((0, 0), (w / x, h / y))

        self._middleVec = pg.math.Vector2(0.5, 0.5)
        self._texts, self._currentPositions = getTextAndPos(self._numMagnets)

        self._controlManager["textRedTorque"] = pw.TextBox((0.45, 0.0), (0.4, 0.1))
        self._controlManager["textRedTorque"].setText("RED is torque vector.")

        self._controlManager["textWhitePos"] = pw.TextBox((0.45, 0.1), (0.4, 0.1))
        self._controlManager["textWhitePos"].setText("WHITE is position vector.")

        self._controlManager["textRealtime"] = pw.TextBox((0.6, 0.2), (0.3, 0.1))
        self._controlManager["textSimtime"] = pw.TextBox((0.6, 0.3), (0.3, 0.1))
        self._controlManager["textDt"] = pw.TextBox((0.6, 0.4), (0.3, 0.1))
        self._controlManager["motorAngle"] = pw.TextBox((0.6, 0.5), (0.3, 0.1))
        self._controlManager["motorSpeed"] = pw.TextBox((0.6, 0.6), (0.3, 0.1))
        self._controlManager["motorTorqueAngle"] = pw.TextBox((0.6, 0.7), (0.3, 0.1))
        self._controlManager["motorTorque"] = pw.TextBox((0.6, 0.8), (0.3, 0.1))

        self._controlManager.update()

    def renderArrow(self, i: Interface):
        arrowDelta = pg.math.Vector2(0.4, 0)
        motorVec = arrowDelta.rotate_rad(i.angleMotor)
        self._controlManager["freeDraw"].arrow(self._middleVec, self._middleVec + motorVec, 3, (255, 255, 255))

        arrowDelta *= 0.7
        torqueVec = arrowDelta.rotate_rad(i.angleTorque)
        self._controlManager["freeDraw"].arrow(self._middleVec, self._middleVec + torqueVec, 3, (255, 0, 0))


    def update(self, i: Interface):
        if not self._controlManager.isRunning():
            return False

        self._controlManager["textRealtime"].setText(f"Real time: {perf_counter() - self._t0:.3f} s.")
        self._controlManager["textSimtime"].setText(f"Simulation Time: {i.simtime:.3f} s.")
        self._controlManager["textDt"].setText(f"Delta Time: {i.dt * 1000 * 1000} us.")
        self._controlManager["motorAngle"].setText(f"Angle: {i.angleMotor:.3f} rad.")
        self._controlManager["motorSpeed"].setText(f"Angular Velocity: {i.angularVelocity:.3f} rad/s.")
        self._controlManager["motorTorqueAngle"].setText(f"Torque Angle: {i.angleTorque:.3f} rad.")
        self._controlManager["motorTorque"].setText(f"Torque: {i.forceTorque:.3f} .")

        self._controlManager["freeDraw"].fill((0, 0, 0))

        self.renderArrow(i)

        for (text, pos) in zip(self._texts, self._currentPositions):
            pos -= self._middleVec
            pos *= 1.1
            pos += self._middleVec
            self._controlManager["freeDraw"].text(pos, text, 18, (255, 255, 255), (0, 0, 0))

        self._controlManager["freeDraw"].circle(self._middleVec, 0.4, (255, 255, 255))

        self._controlManager.update()
        return True