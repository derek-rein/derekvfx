import nuke

def cameraLink():
        hexColour = int('%02x%02x%02x%02x%02x' % (1*255,0*255,0*255,1),16)
        n=nuke.createNode("NoOp")
        n["hide_input"].setValue(True)
        n["tile_color"].setValue(hexColour)
        n.setName('CameraLink')
        n.setInput(0, nuke.toNode('CameraLink'))

def deepLink():
        hexColour = int('%02x%02x%02x%02x%02x' % (0*255,0*255,1*255,1),16)
        n=nuke.createNode("NoOp")
        n["hide_input"].setValue(True)
        n["tile_color"].setValue(hexColour)
        n.setName('DeepLink')
        n.setInput(0, nuke.toNode('DeepLink'))

def plateLink():
        hexColour = int('%02x%02x%02x%02x%02x' % (0*255,1*255,0*255,1),16)
        n=nuke.createNode("NoOp")
        n["hide_input"].setValue(True)
        n["tile_color"].setValue(hexColour)
        n.setName('PlateLink')
        n.setInput(0, nuke.toNode('PlateLink'))
