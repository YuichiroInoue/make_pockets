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
        ui = app.userInterface
        ui.messageBox('Hello script')

        #doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = design.rootComponent

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        lines = sketch.sketchCurves.sketchLines

        point1 = adsk.core.Point3D.create(5, 5, 0)
        point2 = adsk.core.Point3D.create(-5, 5, 0)

        lines.addByTwoPoints(point1, point2)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
