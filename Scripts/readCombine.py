import nuke
import re
from collections import OrderedDict

def multi_read_combine():
    images = nuke.selectedNodes('Read')
    if len(images) < 2:
        nuke.message("Please select at least 2 Read Nodes")
        return

    # Custom dialogue for regex input
    p = nuke.Panel('Pass Name Extraction')
    p.addSingleLineInput('Regex:', '')
    p.addButton('Cancel')
    p.addButton('OK')

    if p.show():
        user_regex = p.value('Regex:')
    else:
        return

    passes_dict = OrderedDict()
    primary_node = None

    for img in images:
        nuke.autoplace(img)
        file_path = img['file'].value()
        file_name = file_path.split('/')[-1].split('.')[0]

        if user_regex:
            match = re.search(user_regex, file_name)
            pass_name = match.group(1) if match else 'undefined'
        else:
            # Default to original functionality
            pass_name = file_name.split('_')[-2]

        if pass_name == 'primary':
            primary_node = img
        else:
            passes_dict[pass_name] = img

    if primary_node:
        passes_dict['primary'] = primary_node
        passes_dict.move_to_end('primary', last=False)

    pipe2 = next(iter(passes_dict.values()))
    for pass_name, img in list(passes_dict.items())[1:]:
        shuffle = nuke.nodes.ShuffleCopy(name=f"shuffle_{pass_name}")
        shuffle.setInput(0, pipe2)
        shuffle.setInput(1, img)

        nuke.Layer(pass_name, [f"{pass_name}.{c}" for c in 'rgb'])

        shuffle['out2'].setValue(pass_name)
        shuffle['red'].setValue('red2')
        shuffle['green'].setValue('green2')
        shuffle['blue'].setValue('blue2')
        shuffle['alpha'].setValue('alpha2')
        shuffle['black'].setValue('red')
        shuffle['white'].setValue('green')
        shuffle['red2'].setValue('blue')
        shuffle['green2'].setValue('alpha')

        pipe2 = shuffle

    nuke.message(f"Combined {len(passes_dict)} passes.")