
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

        labels = [
            "RED is torque vector.",
            "WHITE is position vector.",

            "Motor simulation step: 1 us.",
            "Simulation time: ",
            "Motor Angle: ",
            "Motor Speed: ",
            "Motor Torque: ",
            "Motor Torque Angle: "

        ]
        self._controlManager["textBoxes"] = pw.TextBoxes((0.45, 0.0), (0.55, 1.0), labels = labels)

        alignments = [pw.TextBox.AlignmentHorizontal.LEFT] * 8
        self._controlManager["textBoxes"].setAlignments(horizontal=alignments)

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

        self._controlManager["textBoxes"].setText(f"Simulation Time: {i.simtime:.3f} s.", 3)
        self._controlManager["textBoxes"].setText(f"Angle: {i.angleMotor:.3f} rad.", 4)
        self._controlManager["textBoxes"].setText(f"Angular Velocity: {i.angularVelocity:.3f} rad/s.", 5)
        self._controlManager["textBoxes"].setText(f"Torque: {i.forceTorque:.3f} .", 6)
        self._controlManager["textBoxes"].setText(f"Torque Angle: {i.angleTorque:.3f} rad.", 7)

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