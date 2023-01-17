# Import the necessary modules
import nuke
from PySide2 import QtWidgets

# Define the function to align nodes
def align_nodes(horizontal=True):
    # Get the selected nodes
    selected_nodes = nuke.selectedNodes()
    
    # Check if there are at least two nodes selected
    if len(selected_nodes) < 2:
        nuke.message("Please select at least two nodes to align.")
        return
    
    # Calculate the average x or y position of the selected nodes, depending on the alignment
    if horizontal:
        avg_pos = sum(node.xpos() for node in selected_nodes) / len(selected_nodes)
    else:
        avg_pos = sum(node.ypos() for node in selected_nodes) / len(selected_nodes)
    
    # Align the selected nodes to the calculated average position
    for node in selected_nodes:
        if horizontal:
            node.setXpos(int(avg_pos))
        else:
            node.setYpos(int(avg_pos))

# Create a widget with two buttons for aligning nodes horizontally or vertically
class AlignmentWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Create the buttons
        self.horizontal_button = QtWidgets.QPushButton("Align Horizontally")
        self.vertical_button = QtWidgets.QPushButton("Align Vertically")

        # Connect the buttons to the align_nodes() function
        self.horizontal_button.clicked.connect(lambda: align_nodes(horizontal=True))
        self.vertical_button.clicked.connect(lambda: align_nodes(horizontal=False))

        # Create a layout for the buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.horizontal_button)
        button_layout.addWidget(self.vertical_button)

        # Set the layout for the widget
        self.setLayout(button_layout)

widget = AlignmentWidget()
widget.show()