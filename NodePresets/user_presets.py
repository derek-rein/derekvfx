import nuke
def nodePresetsStartup():
  nuke.setUserPreset("ContactSheet", "contactSheet", {'indicators': '2', 'width': '{input.width*columns}', 'rows': '1', 'columns': '2', 'height': '{input.height*rows}'})
  nuke.setUserPreset("Copy", "BLANK", {'bbox': 'B'})
  nuke.setUserPreset("Expression", "STMAP", {'expr2': '0', 'expr3': '0', 'expr0': '(x+.5) / width', 'expr1': '(y+.5) / height'})
  nuke.setUserPreset("Expression", "RADIAL", {'temp_name0': 'zz', 'selected': 'true', 'label': '[knob expr3]', 'expr2': 'zz', 'expr0': 'zz', 'expr1': 'zz', 'temp_expr0': 'sqrt((x-width/2)**2 + (y-height/2)**2)/width'})
  nuke.setUserPreset("Expression", "ISNAN", {'expr3': 'max(isnan(r),isnan(g),isnan(b))', 'label': '[knob expr3]'})
  nuke.setUserPreset("Expression", "RECIPROCAL", {'expr2': '1/b', 'expr0': '1/r', 'expr1': '1/g', 'selected': 'true', 'label': '[knob expr3]'})
  nuke.setUserPreset("Expression", "FRINGE", {'expr3': '4*(1-a)*a', 'selected': 'true', 'label': '[knob expr3]'})
  nuke.setUserPreset("Expression", "FIX_EXP", {'channel3': 'alpha', 'temp_name0': 'z', 'selected': 'true', 'expr2': '(b < 0.00001 && b > 0) ? z : b', 'expr0': '(r < 0.00001 && r > 0)  ? z : r', 'expr1': '(g < 0.00001 && g > 0) ? z : g', 'temp_expr0': '0.00001 '})
  nuke.setUserPreset("Expression", "COLOR", {'expr2': '(1/(r*.3+g*.59+b*.11))*b', 'expr0': '(1/(r*.3+g*.59+b*.11))*r', 'expr1': '(1/(r*.3+g*.59+b*.11))*g', 'selected': 'true'})
  nuke.setUserPreset("Expression", "UV", {'expr0': '(x + .5) / width', 'expr1': '(y + .5) / height', 'label': 'UV', 'selected': 'true'})
  nuke.setUserPreset("Expression", "NOT_BLACK", {'expr3': 'r + g + b == 0 ? 0 : 1', 'selected': 'true'})
  nuke.setUserPreset("Remove", "KEEP_RGBA", {'channels': 'rgba', 'operation': 'keep'})
