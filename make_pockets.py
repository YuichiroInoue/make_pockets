# Author-Yuichiro
# Description-make huge number of pockets

import adsk.core
import adsk.fusion
import adsk.cam
import traceback
import os

app = adsk.core.Application.get()
# doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
design = app.activeProduct
# Get the root component of the active design.
rootComp = design.rootComponent


class MainBody:
    def __init__(self, size, depth):
        self._size = size
        self._depth = depth

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self_size = value

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = depth

    # main_extrude = adsk.fusion.ExtrudeFeature

    def build(self):
        # Create a new sketch on the xy plane.
        body_sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = body_sketches.add(xyPlane)
        self._sketch = sketch
        lines = sketch.sketchCurves.sketchLines

        # make square
        size = self._size

        point1 = adsk.core.Point3D.create(size/2, size/2, 0)
        point2 = adsk.core.Point3D.create(-size/2, size/2, 0)
        point3 = adsk.core.Point3D.create(-size/2, -size/2, 0)
        point4 = adsk.core.Point3D.create(size/2, -size/2, 0)

        lines.addByTwoPoints(point1, point2)
        lines.addByTwoPoints(point2, point3)
        lines.addByTwoPoints(point3, point4)
        lines.addByTwoPoints(point4, point1)

        # extrude
        extrudes = rootComp.features.extrudeFeatures
        prof = sketch.profiles.item(0)
        distance = adsk.core.ValueInput.createByReal(self._depth*-1)
        extrude1 = extrudes.addSimple(
            prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        base_body = extrude1.bodies.item(0)
        base_body.name = 'base'

        # health check
        health = extrude1.healthState
        if (health == adsk.fusion.FeatureHealthStates.WarningFeatureHealthState
                or health == adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState):
            message = extrude1.errorOrWarningMessage
        else:
            self._extrude = extrude1
            pass

    def delete(self):
        self._extrude.deleteMe()
        self._sketch.deleteMe()


class Pocket:
    def __init__(self, size, depth, corner):
        self._size = size
        self._depth = depth
        self._corner = corner

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self_size = value

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = depth

    @property
    def corner(self):
        return self._corner

    @corner.setter
    def corner(self, value):
        self._corner = corner

    def build(self):
        # Create a new sketch on the xy plane.
        body_sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = body_sketches.add(xyPlane)
        self._sketch = sketch
        lines = sketch.sketchCurves.sketchLines
        arcs = sketch.sketchCurves.sketchArcs
        size = self._size
        corner = self._corner

        point1 = adsk.core.Point3D.create(size/2, size/2, 0)
        point2 = adsk.core.Point3D.create(-size/2, size/2, 0)
        point3 = adsk.core.Point3D.create(-size/2, -size/2, 0)
        point4 = adsk.core.Point3D.create(size/2, -size/2, 0)

        line1 = lines.addByTwoPoints(point1, point2)
        line2 = lines.addByTwoPoints(point2, point3)
        line3 = lines.addByTwoPoints(point3, point4)
        line4 = lines.addByTwoPoints(point4, point1)

        arcs.addFillet(line1, point1, line4, point1, corner)
        arcs.addFillet(line1, point2, line2, point2, corner)
        arcs.addFillet(line2, point3, line3, point3, corner)
        arcs.addFillet(line3, point4, line4, point4, corner)

        extrudes = rootComp.features.extrudeFeatures
        extrude2 = extrudes.addSimple(sketch.profiles.item(0), adsk.core.ValueInput.createByReal(self._depth*-1),
                                      adsk.fusion.FeatureOperations.CutFeatureOperation)

        # health check
        health = extrude2.healthState
        if (health == adsk.fusion.FeatureHealthStates.WarningFeatureHealthState
                or health == adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState):
            message = extrude2.errorOrWarningMessage
        else:
            self._extrude = extrude2
            pass

    def delete(self):
        self._extrude.deleteMe()
        self._sketch.deleteMe()


def run(context):
    ui = None
    try:

        output_dir = os.getenv("HOMEDRIVE") + \
            os.getenv("HOMEPATH")+"/desktop/fusion360api/"
        os.makedirs(output_dir, exist_ok=True)

        main_body = MainBody(5.0, 3.0)
        main_body.build()

        size = 3.0
        depth = 2.0
        corner = 1.0

        for i in range(10):
            depth = round(1.0+i*0.1, 4)
            for j in range(50):
                corner = round(0.5+j*0.01, 4)
                # make pocket
                pocket = Pocket(size, depth, corner)
                pocket.build()

                exportMgr = design.exportManager

                # export
                filename = str(size)+"_"+str(corner)+"_"+str(depth)+".step"
                stepOptions = exportMgr.createSTEPExportOptions(
                    output_dir+filename)
                res = exportMgr.execute(stepOptions)

                # clean up
                pocket.delete()

        main_body.delete()

    except Exception as e:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        else:
            print(e)
            pass
