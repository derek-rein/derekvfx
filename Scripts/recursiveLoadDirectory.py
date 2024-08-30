import nuke
import os
import re

def is_image_file(filename):
    # Add or remove extensions as needed
    image_extensions = ['.exr', '.dpx', '.jpg', '.jpeg', '.png', '.tiff', '.tif']
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def get_sequence_pattern(filename):
    # Pattern detection for name.####.extension or name_####.extension
    match = re.match(r'(.+[._])(\d+)(\.\w+)$', filename)
    if match:
        base, number, ext = match.groups()
        return f"{base}{'#' * len(number)}{ext}"
    return filename

def find_and_load_sequences(directory):
    for root, dirs, files in os.walk(directory):
        image_files = [f for f in files if is_image_file(f)]
        if image_files:
            # Group files by their sequence pattern
            sequences = {}
            for file in image_files:
                pattern = get_sequence_pattern(file)
                if pattern not in sequences:
                    sequences[pattern] = []
                sequences[pattern].append(file)
            
            # Create Read nodes for each sequence
            for pattern, seq_files in sequences.items():
                if len(seq_files) > 1 and '#' in pattern:  # It's a sequence
                    file_path = os.path.join(root, pattern)
                    read_node = nuke.createNode('Read')
                    read_node['file'].setValue(file_path)
                    
                    # Set frame range
                    frame_numbers = [int(re.search(r'(\d+)(?=\.\w+$)', f).group(1)) for f in seq_files]
                    first_frame = min(frame_numbers)
                    last_frame = max(frame_numbers)
                    read_node['first'].setValue(first_frame)
                    read_node['last'].setValue(last_frame)
                    
                    print(f"Loaded sequence: {file_path}")
                else:  # Single image
                    file_path = os.path.join(root, seq_files[0])
                    read_node = nuke.createNode('Read')
                    read_node['file'].setValue(file_path)
                    print(f"Loaded single image: {file_path}")

# Usage
directory = nuke.getFilename('Select Directory', 'Directory')
if directory:
    find_and_load_sequences(directory)
else:
    print("No directory selected.")
