import nuke
def nodePresetsStartup():
  nuke.setUserPreset("ContactSheet", "contactSheet", {'indicators': '2', 'width': '{input.width*columns}', 'rows': '1', 'columns': '2', 'height': '{input.height*rows}'})
  nuke.setUserPreset("Expression", "notBlack", {'expr3': 'r + g + b == 0 ? 0 : 1', 'selected': 'true'})
