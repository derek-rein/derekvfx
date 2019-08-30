import nuke
import _nukemath as m
import nukescripts
import threading
import math
import time


"""
# add this to menu.py file

import matrixInverter
nuke.menu("Nuke").addCommand('Scripts/Matrix Inverter', 'matrixInverter.main()')


"""

def htmlcolor(r, g, b):
    def clamp(x):
        return max(0, min(x, 255))

    return int("{0:02x}{1:02x}{2:02x}{2:02x}".format(clamp(r), clamp(g), clamp(b), 0), 16)


class DerekVFXMatrixInverterPanel(nukescripts.PythonPanel):
    """
    Creates a new axis node with an inverted matrix transformation
    """
    data = dict()
    data["scriptName"] = "DerekVFX - Matrix Inverter"
    data["scriptVersion"] = "1.3"

    def __init__(self):
        nukescripts.PythonPanel.__init__(self, '{0} v{1}'.format(self.data["scriptName"], self.data["scriptVersion"]))
        self.knob_first_frame = nuke.Int_Knob("ff", "first frame")
        self.knob_last_frame = nuke.In
 t_Knob("lf", "last frame")
        self.checkbox_TRS = nuke.Boolean_Knob('trs_mode', "Set TRS Keys", True)
        self.checkbox_TRS.setFlag(nuke.STARTLINE)
        self.div1 = nuke.Text_Knob("divider1", "")
        self.btn_create = nuke.PyScript_Knob("createBtn", "create node")

        for i in [self.knob_first_frame, self.knob_last_frame, self.checkbox_TRS, self.div1, self.btn_create]:
            self.addKnob(i)

        # SET INITIAL VALUES
        self.knob_first_frame.setValue(int(nuke.root()["first_frame"].value()))
        self.knob_last_frame.setValue(int(nuke.root()["last_frame"].value()))

        self.setMinimumSize(250, 150)

    # Set knobChanged commands.
    def knobChanged(self, knob):
        if knob is self.btn_create:
            try:
                self.invertMatrix(self.checkbox_TRS.value())
                self.hide()
            except Exception as e:
                print e
                self.hide()

    def
  invertMatrix(self, mode):  # Get the selected node.
        try:
            source_axis = nuke.selectedNode()
        except ValueError:
            nuke.message("Select a node.")
            return

        if source_axis.Class() not in ['Axis', "Axis2", 'Camera2', 'Light', 'Light2', 'Camera']:
            nuke.message("Select a 3D node.")
            return

        source_axis["selected"].setValue(False)

        # SET VALUES
        destination_axis = nuke.createNode('Axis2')
        destination_axis.setName('{}_inverted'.format(source_axis['name'].value()))
        destination_axis["tile_color"].setValue(htmlcolor(0, 255, 0))
        if mode:
            # RESET ANIMATION
            # destination_axis['translate'].clearAnimated()
            # destination_axis['rotate'].clearAnimated()
            # destination_axis['scaling'].clearAnimated()
            destination_axis['translate'].setAnimated()
            destination_axis['rota
 te'].setAnimated()
            destination_axis['scaling'].setAnimated()
        else:
            destination_axis['useMatrix'].setValue(True)
            destination_axis['matrix'].setAnimated()

        # set the keys
        task = nuke.ProgressTask("Inverting Matrix")
        task.setMessage("Setting Keys")
        first, last = self.knob_first_frame.value(), self.knob_last_frame.value()

        def setKeys():
            for frame in range(first, last):
                if task.isCancelled():
                    nuke.executeInMainThread(nuke.message, args=("Cancelled"))
                    break
                source_axis_values = source_axis['matrix'].valueAt(frame)

                # INIT MATRIX OBJECT
                matrix = m.Matrix4()
                matrix.makeIdentity()  # probably don't need this
                for k, v in enumerate(source_axis_values):
                    matrix[k] = v  # this is the only way to set values on nuke m
 atrix 4 object

                matrix = matrix.inverse()

                if mode:
                    '''
                    ANIMATE THE TRANSLATE SCALE AND ROTATION KNOBS
                    '''
                    matrix.transpose()  # row become columns and vice versa
                    mTranslate = nuke.math.Matrix4(matrix)
                    mTranslate.translationOnly()
                    mRotate = nuke.math.Matrix4(matrix)
                    mRotate.rotationOnly()
                    mScale = nuke.math.Matrix4(matrix)
                    mScale.scaleOnly()

                    rotateRad = mRotate.rotationsZXY()
                    # convert from radians to degrees
                    rotate = (math.degrees(rotateRad[0]), math.degrees(rotateRad[1]), math.degrees(rotateRad[2]))

                    destination_axis['translate'].setValueAt(mTranslate[12], frame, 0)
                    destination_axis['translate'].setValueAt(mTranslate[13], fram
 e, 1)
                    destination_axis['translate'].setValueAt(mTranslate[14], frame, 2)
                    destination_axis['rotate'].setValueAt(rotate[0], frame, 0)
                    destination_axis['rotate'].setValueAt(rotate[1], frame, 1)
                    destination_axis['rotate'].setValueAt(rotate[2], frame, 2)
                    destination_axis['scaling'].setValueAt(mScale.xAxis().x, frame, 0)
                    destination_axis['scaling'].setValueAt(mScale.yAxis().y, frame, 1)
                    destination_axis['scaling'].setValueAt(mScale.zAxis().z, frame, 2)

                else:
                    '''
                    ANIMATE THE MATRIX KNOB
                    '''
                    for index in range(0, 16):
                        value = matrix[index]  # iterating directly on the matrix causes indexing errors
                        destination_axis['matrix'].setValueAt(value, frame, index)

                task.setP
 rogress(((frame-first)/(last-first))*100)

        threading.Thread(None, setKeys).start()


# Run main script.
def main():
    DerekVFXMatrixInverterPanel().showModal()

