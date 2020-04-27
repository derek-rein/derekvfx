import nuke

# ADD THE FOLLOWING TO menu.py
#import elbows
#nuke.menu("Nuke").addCommand('Scripts/Elbows', 'elbows.main()', "shift+alt+e")

def nodeHasMask(node):
    return node.knobs().has_key('maskChannelMask')


def getMinInputs(node):
    min_inputs = node.minInputs()
    return (min_inputs - 1) if nodeHasMask(node) and min_inputs > 0 else min_inputs


def getPos(node):
    return node.xpos(), node.ypos()


def getSize(node):
    return node.screenWidth() / 2, node.screenHeight() / 2


def checkUnder(src, dst):
    """
    True if source is within 1/2 the max of both src and dst widths on x axis
    """
    m = getPos(src)[0] + getSize(src)[0]
    d = getPos(dst)[0] + getSize(dst)[0]
    threshold = max(getSize(src)[0], getSize(dst)[0])  # threshold is max of half widths
    return abs(m - d) < threshold


def align(dot, dst, mer):
    """
    Aligns dots in a parallel way
    """
    size_dot_x, size_dot_y = getSize(dot)
    x = getPos(dst)[0] + getSize(dst)[0] - size_dot_x
    y = getPos(mer)[1] + getSize(mer)[1] - size_dot_y
    dot.setXYpos(x, y)
    return x, y


def align_overhead(dot, dep, node):  # src = dep
    """
    Create and align dot overhead
    """
    size_dot_x, size_dot_y = getSize(dot)
    x = getPos(node)[0] + getSize(node)[0] - size_dot_x
    y = getPos(dep)[1] + getSize(dep)[1] - size_dot_y
    dot.setXYpos(x, y)
    return x, y


def elbows(node):
    if len(node.dependencies(nuke.INPUTS)) == 1:
        """
        The node has a single input, so do an overhead elbow
        """
        dep = node.input(0)
        if dep is None:
            return  # It's not connected to anything, exit

        if not checkUnder(node, dep):  # Don't do anything if we're already under it
            if dep.Class() == 'Dot':  # If its a dot, don't make another one
                dot = nuke.nodes.Dot()
                dot.setInput(0, dep)
                align_overhead(dot, dep, node)
                node.setInput(0, dot)
                return [dot]

        else:
            node.setSelected(False)
            dep.setSelected(True)
            dot = nuke.createNode('Dot', inpanel=False)
            dot.setYpos(dot.ypos() + node.screenHeight() * 2)
            dot2 = nuke.nodes.Dot()
            align_overhead(dot2, dot, node)
            dot2.setInput(0, dot)
            node.setInput(0, dot2)
            return [dot, dot2]

    elif len(node.dependencies(nuke.INPUTS)) > 1:
        """
        The node has multiple inputs, create parallel elbows
        """
        if node.Class() in ('ContactSheet', 'Switch', 'Merge2',
                            'Merge', 'Blend', 'Dissolve', 'Keymix',
                            'Copy', 'AddMix', 'CopyBBox', 'ChannelMerge'):
            dots = []
            try:
                child = node.dependent(nuke.INPUTS)[0]  # check if there is a connected node
            except:
                child = None
            for input in range(node.inputs()):
                if node.Class() not in ('ContactSheet', 'Switch'):
                    if input in [2]:  # input 2 is the mask, skip it
                        continue
                dep = node.input(input)
                if dep is not None:
                    if not checkUnder(node, dep):
                        dep.setSelected(True)
                        dot = nuke.createNode('Dot', inpanel=False)
                        dots.append(dot)
                        dep.setSelected(False)
                        align(dot, dep, node)
                        dot.setSelected(False)
                if child is not None:
                    child.setInput(0, node)
                return dots


def main():
    nodes = nuke.selectedNodes()
    if len(nodes) == 1:
        """
        A single node selection assumes an elbow joint on non mask inputs.
        """
        elbows(nodes[0])

    elif len(nodes) > 1:
        """
        If multiple nodes are selected, it assumes we want to add them together.
        """
        # empty lists are false, checking to see if these nodes are not already connected
        if all(not n.dependent(nuke.INPUTS) for n in nodes):
            m = nuke.createNode('Merge2')
            last = nodes[-1]  # get the node that the merge should go under
            m['operation'].setValue('plus')
            m['bbox'].setValue('union')
            m.setYpos(max(n.ypos() for n in nodes) + m.screenHeight() * 3)  # set Ypos under the lowest of selection
            m.setXpos(getPos(last)[0] + getSize(last)[0] - getSize(m)[0])  # set Xpos to the last selected

            for i, node in enumerate(nodes):
                if i >= 2:
                    i += 1
                m.setInput(i, node)
            dots = elbows(m)
            for d in dots:
                d.setSelected(True)
            m.setSelected(True)