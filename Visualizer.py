
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

    def close(self):
        self._controlManager.close()

    def setup(self):
        x, y = self._controlManager.getSize()
        x, y = 1920, 1080
        w, h = 880, 900
        self._controlManager["freeDraw"] = pw.FreeDraw((0, 0), (w / x, h / y))

        self._middleVec = pg.math.Vector2(0.5, 0.5)
        self._texts, self._currentPositions = getTextAndPos(self._numMagnets)

        labels = [
            "Motor simulation step:",
            "Simulation time:",
            "Motor Angle:",
            "Motor Speed:",
            "Motor Torque:"
        ]

        alignments = [pw.TextBox.AlignmentHorizontal.LEFT] * 5
        self._controlManager["textBoxesLeft"] = pw.TextBoxes((0.45, 0.0), (0.3, 0.3), labels = labels)
        self._controlManager["textBoxesLeft"].setAlignments(horizontal=alignments)

        self._controlManager["textBoxesRight"] = pw.TextBoxes((0.75, 0.0), (0.25, 0.3), labels = [""] * 5)
        self._controlManager["textBoxesRight"].setAlignments(horizontal=alignments)
        self._controlManager["textBoxesRight"].setText("1 us", 0)

        plot = pw.Plot((0.45, 0.3), (0.55, 0.3))
        plot.setTitle("Motor Position")
        plot.setXLabel("Time (ms)")
        plot.setYLabel("Position (Rad)")
        self._controlManager["plotPosition"] = plot

        plot = pw.Plot((0.45, 0.6), (0.55, 0.3))
        plot.setTitle("Motor Velocity")
        plot.setXLabel("Time (ms)")
        plot.setYLabel("Velocity (Rad/s)")
        self._controlManager["plotVelocity"] = plot

        self._controlManager.update()

    def renderArrow(self, i: Interface):
        arrowDelta = pg.math.Vector2(0.4, 0)
        motorVec = arrowDelta.rotate_rad(i.angleMotor)
        self._controlManager["freeDraw"].arrow(self._middleVec, self._middleVec + motorVec, 3, (255, 255, 255))

    def update(self, i: Interface):
        if not self._controlManager.isRunning():
            return False

        maxLength = 2500
        plotT = round(i.simtime * 1000.0, 3)
        self._controlManager["plotPosition"].addValue(plotT, i.angleMotor, 0, maxLength)
        self._controlManager["plotPosition"].addValue(plotT, i.angleSetpoint, 1, maxLength)

        self._controlManager["plotVelocity"].addValue(plotT, i.angularVelocity, 0, maxLength)
        self._controlManager["plotVelocity"].addValue(plotT, i.angularVelocitySetpoint, 1, maxLength)

        self._controlManager["textBoxesRight"].setText(f"{i.simtime:.3f} s", 1)
        self._controlManager["textBoxesRight"].setText(f"{i.angleMotor:.3f} rad", 2)
        self._controlManager["textBoxesRight"].setText(f"{i.angularVelocity:.3f} rad/s", 3)
        self._controlManager["textBoxesRight"].setText(f"{i.forceTorque:.3f} ", 4)

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