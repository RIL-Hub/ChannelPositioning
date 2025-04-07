import numpy as np

def get_crystal_locs(crystal_width, crystal_pitch, repeats):
    
    panel_width = crystal_width * repeats + crystal_pitch * (repeats-1)
    step_size = crystal_width + crystal_pitch
    crystal_locs = np.arange(0, panel_width, step_size) + crystal_width/2 - panel_width/2
    
    return crystal_locs


def get_crystal_map(crystal_xlocs, crystal_ylocs, crystal_zlocs, panel_nodes, boards_in_node):
    '''
    crystal_map has row structure: Node, Board, x, y, z
    where x, y, z denotes the crystal center for that Node-Board combo.
    '''
    
    crystal_map = np.empty([len(panel_nodes)*len(boards_in_node), 5])
    
    crystal_index = 0
    for node_index in range(len(panel_nodes)):
        for board_index in range(len(boards_in_node)):
            
            node_number = panel_nodes[node_index]
            board_number = boards_in_node[board_index]
            
            x = crystal_xlocs[node_index]
            y = crystal_ylocs
            z = crystal_zlocs[board_index]
            
            crystal_map[crystal_index, 0] = node_number
            crystal_map[crystal_index, 1] = board_number
            crystal_map[crystal_index, 2:]  = [x, y, z]
            
            crystal_index += 1
    
    return crystal_map


def build_electrode_map(channels_per_crystal, channel_dict,
                        anode_positions, cathode_positions,
                        crystal_z_width, orientation, panel_number):
    '''
    electrode_map has row structure: RENA, Channel, x, y, z
    where x, y, z denotes the channel position relative to crystal center.
    '''
    
    if panel_number == 1:
        sign = 1
        if orientation == 'bottom':
            sign = -1
            anode_positions = anode_positions[::-1]
    else: # panel_number == 2:
        sign = -1
        cathode_positions = cathode_positions[::-1]
        if orientation == 'top':
            sign = 1
            anode_positions = anode_positions[::-1]
    
    electrode_index = 0
    electrode_map = np.empty([channels_per_crystal, 5])
    for RENA in [0, 1]:
        for channel_number in np.arange(1, channels_per_crystal+1):
            electrode_key = str(int(RENA)) + '_' + str(int(channel_number))
            
            if electrode_key in channel_dict:
                
                electrode = channel_dict[electrode_key]
                polarity = electrode[0]
                electrode_number = int(electrode[1:])
                
                if polarity == 'A':
                    x = anode_positions[electrode_number-1]
                    relative_loc = [x, 0, sign*(crystal_z_width/2)]
                else: # polarity = 'C':
                    y = cathode_positions[electrode_number-1]
                    relative_loc = [0, y, sign*(-crystal_z_width/2)]
                
                electrode_map[electrode_index, 0] = RENA
                electrode_map[electrode_index, 1] = channel_number
                electrode_map[electrode_index, 2:] = relative_loc
                
                electrode_index += 1

    return electrode_map


def build_NodeBoard_dict(channel_map):
    """Builds a dictionary where the key is 'C0_C1' and the value is rows matching those first two columns."""
    NodeBoard_dict = {}
    
    for row in channel_map:
        key = f"{int(row[0])}_{int(row[1])}"
        if key not in NodeBoard_dict:
            NodeBoard_dict[key] = []
        NodeBoard_dict[key].append(row)
    
    # Convert lists to NumPy arrays for easier slicing
    for key in NodeBoard_dict:
        NodeBoard_dict[key] = np.array(NodeBoard_dict[key])
    
    return NodeBoard_dict

