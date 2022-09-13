import nuke
def nodePresetsStartup():
  nuke.setUserPreset("Copy", "BLANK", {'bbox': 'B'})
  nuke.setUserPreset("ContactSheet", "contactSheet", {'indicators': '2', 'width': '{input.width*columns}', 'rows': '1', 'columns': '2', 'height': '{input.height*rows}'})
  nuke.setUserPreset("Expression", "notBlack", {'expr3': 'r + g + b == 0 ? 0 : 1', 'selected': 'true'})
  nuke.setUserPreset("Expression", "STMAP", {'expr0': '(x-.5) /width', 'expr1': '(y-.5) /height'})
  nuke.setUserPreset("Expression", "RADIAL", {'temp_name0': 'zz', 'selected': 'true', 'label': '[knob expr3]', 'expr2': 'zz', 'expr0': 'zz', 'expr1': 'zz', 'temp_expr0': 'sqrt((x-width/2)**2 + (y-height/2)**2)/width'})

