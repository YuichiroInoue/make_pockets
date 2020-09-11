# Author-Yuichiro
# Description-make huge number of pockets

import adsk.core
import adsk.fusion
import adsk.cam
import traceback


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        # ui = app.userInterface
        # ui.messageBox('Hello script')

        #doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        lines = sketch.sketchCurves.sketchLines

        # make square
        size = 5.0

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
        distance = adsk.core.ValueInput.createByReal(-3)
        extrude1 = extrudes.addSimple(
            prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

        base_body = extrude1.bodies.item(0)
        base_body.name = 'base'

        # health check
        health = extrude1.healthState
        if (health == adsk.fusion.FeatureHealthStates.WarningFeatureHealthState
                or health == adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState):
            message = extrude1.errorOrWarningMessage

        # make pocket
        size = 3.0
        corner = 1.0
        depth = 2.0

        sketch2 = sketches.add(xyPlane)
        lines = sketch2.sketchCurves.sketchLines
        arcs = sketch2.sketchCurves.sketchArcs

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

        extrudes2 = rootComp.features.extrudeFeatures

        extrude2 = extrudes2.addSimple(sketch2.profiles.item(0), adsk.core.ValueInput.createByReal(depth*-1),
                                       adsk.fusion.FeatureOperations.CutFeatureOperation)

        # health check
        health = extrude2.healthState
        if (health == adsk.fusion.FeatureHealthStates.WarningFeatureHealthState
                or health == adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState):
            message = extrude2.errorOrWarningMessage

    except Exception as e:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
        else:
            print(e)
            pass
