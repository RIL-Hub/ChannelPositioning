import numpy as np
import source.mapping as mapping
import source.plotting as plotting


def main():
    
    
    ########## USER SETTINGS ##########
    
    
    # --- Geometric Parameters --- #
    
    output_file_name = 'coords.pos'
    output_dir = 'output' # relative or absoute path
    channel_map_file = 'chanMapHN.cmf' # must be in assests
    output_precision = 3 # number of places after decimal to save
    use_crystal_z = 0 # assign crystal z as elecrtode z? otherwise use true z
    
    panel_1_nodes = [1, 2, 3, 4, 5]  # from smallest x-value to largest
    panel_2_nodes = [10, 9, 8, 7, 6] # from smallest x-value to largest
    top_board_number = 15 # board with largest z-value
    bottom_board_number = 30 # board with smallest z-value
    # WE ASSUME BOARDS ARE CONSECUTIVELY NUMBERED
    boards_in_node = np.arange(top_board_number, bottom_board_number+1)
    
    crystal_x_width = 40 # [mm]
    crystal_y_width = 40 # [mm]
    crystal_z_width = 5 # [mm]
    
    panel_spacing = 204 # [mm], crystalFace-to-crsytalFace distance
    crystal_x_pitch = 0.0 # [mm], edge-to-edge pitch
    crystal_z_pitch = 0.0 # [mm], edge-to-edge pitch
    
    anode_strip_width = 0.1 # [mm], only used for plotting
    anode_strip_pitch = 1 # [mm], center-to-center pitch
    num_anodes_per_crystal = 39
    
    cathode_strip_width = 4.9 # [mm], only used for plotting
    cathode_strip_pitch = 5 # [mm], center-to-center pitch
    num_cathodes_per_crystal = 8
    
    channels_per_crystal = num_anodes_per_crystal + num_cathodes_per_crystal
    
    # --- Plotting Options --- #
    
    plot_crystal_point_map = 0
    plot_crystal_surface_map = 0
    plot_electrode_point_map = 0
    plot_electrode_surface_map = 0
    
    plot_NodeBoard_channels = 0
    NodeBoard_plot_list = ['1_30', '5_17', '10_15']
    
    
    ########## END USER SETTINGS ##########
    
    
    # --- Prepare Channel Map --- #
    '''
    channel_dict has keys of "rena_channel" and values of "electrode" (like "A01" or "C08")
    '''
    
    channel_map = np.genfromtxt('assests/' + channel_map_file, skip_header=1, dtype='object')
    channel_dict = {}
    for entry in channel_map:
        rena = int(entry[0])
        channel_number = int(entry[1])
        electrode = (entry[2]).decode('ascii')
        polarity_channelNumber = '_'.join(str(i) for i in [rena, channel_number])
        channel_dict[polarity_channelNumber] = electrode
    
    
    
    # --- Build Crystal Maps --- #
    
    # build panel 1 map
    panel_1_crystal_xlocs = mapping.get_crystal_locs(crystal_x_width, crystal_x_pitch, len(panel_1_nodes))
    panel_1_crystal_ylocs = panel_spacing/2 + crystal_y_width/2
    panel_1_crystal_zlocs = mapping.get_crystal_locs(crystal_z_width, crystal_z_pitch, len(boards_in_node))
    panel_1_crystal_zlocs = panel_1_crystal_zlocs[::-1]
    
    panel_1_crystal_map = mapping.get_crystal_map(panel_1_crystal_xlocs,
                                                  panel_1_crystal_ylocs,
                                                  panel_1_crystal_zlocs,
                                                  panel_1_nodes, boards_in_node)
    
    # build panel 2 map
    panel_2_crystal_xlocs = mapping.get_crystal_locs(crystal_x_width, crystal_x_pitch, len(panel_2_nodes))
    panel_2_crystal_ylocs = -(panel_spacing/2 + crystal_y_width/2)
    panel_2_crystal_zlocs = mapping.get_crystal_locs(crystal_z_width, crystal_z_pitch, len(boards_in_node))
    panel_2_crystal_zlocs = panel_2_crystal_zlocs[::-1]
    
    # need to sort afterwards as node x-order is reversed as compared to panel 1
    panel_2_crystal_map = mapping.get_crystal_map(panel_2_crystal_xlocs,
                                                  panel_2_crystal_ylocs,
                                                  panel_2_crystal_zlocs,
                                                  panel_2_nodes, boards_in_node)
    sorted_indices = np.argsort(panel_2_crystal_map[:, 0], kind='stable')
    panel_2_crystal_map = panel_2_crystal_map[sorted_indices]



    # --- Build Template Electrode Positions --- #
    
    # cathode positions from C1 -> C8 (smallest y to largest)
    offset = cathode_strip_pitch/2 if num_cathodes_per_crystal % 2 == 0 else anode_strip_pitch
    cathode_positions = np.arange(0, num_cathodes_per_crystal, 1) * cathode_strip_pitch + offset - crystal_y_width/2
    
    # anode positions from A1 -> A39 (smallest x to largest)
    offset = anode_strip_pitch/2 if num_anodes_per_crystal % 2 == 0 else anode_strip_pitch
    anode_positions = np.arange(0, num_anodes_per_crystal) * anode_strip_pitch + offset - crystal_x_width/2
    
    
    
    # --- Build Channel Map --- #
    
    total_number_of_channels = channels_per_crystal * len(boards_in_node) * (len(panel_1_nodes) + len(panel_1_nodes))
    channel_map = np.empty([total_number_of_channels, 7])
    channel_index = 0
    
    # panel 1 map
    # - cathode number increases in the +y direction
    # - top crystal anode number increases in the +x direction
    # - bottom crystal anode number increases in the -x direction
    
    panel_1_top_crystal_electrode_map = mapping.build_electrode_map(channels_per_crystal, channel_dict,
                                                                    anode_positions, cathode_positions,
                                                                    crystal_z_width, 'top', 1)
    
    panel_1_bottom_crystal_electrode_map = mapping.build_electrode_map(channels_per_crystal, channel_dict,
                                                                       anode_positions, cathode_positions,
                                                                       crystal_z_width, 'bottom', 1)
    
    for crystal in panel_1_crystal_map:
        node  = crystal[0]
        board = crystal[1]
        crystal_xyz = crystal[2:]
        
        board_index = board - top_board_number + 1
        # odd board_index means top crystal
        # even board_index means bottom crystal
        if board_index % 2 == 0:
            electrode_map = panel_1_bottom_crystal_electrode_map
        else:
            electrode_map = panel_1_top_crystal_electrode_map
            
        for electrode in electrode_map:
            rena = electrode[0]
            channel = electrode[1]
            electrode_xyz = electrode[2:]
            
            xyz = crystal_xyz + electrode_xyz
            if use_crystal_z:
                xyz[2] = crystal_xyz[2]
            
            channel_map[channel_index, 0:4] = [node, board, rena, channel]
            channel_map[channel_index, 4:]  = xyz
            channel_index += 1
    
    # panel 2 map
    # - cathode number now increase in the -y direction
    # - top crystal anode number now increases in the -x direction
    # - bottom crystal anode number now increases in the +x direction
    
    panel_2_top_crystal_electrode_map = mapping.build_electrode_map(channels_per_crystal, channel_dict,
                                                                    anode_positions, cathode_positions,
                                                                    crystal_z_width, 'top', 2)
    
    panel_2_bottom_crystal_electrode_map = mapping.build_electrode_map(channels_per_crystal, channel_dict,
                                                                       anode_positions, cathode_positions,
                                                                       crystal_z_width, 'bottom', 2)
    
    for crystal in panel_2_crystal_map:
        node  = crystal[0]
        board = crystal[1]
        crystal_xyz = crystal[2:]
        
        board_index = board - top_board_number + 1
        # odd board_index means top crystal
        # even board_index means bottom crystal
        if board_index % 2 == 0:
            electrode_map = panel_2_top_crystal_electrode_map
        else:
            electrode_map = panel_2_bottom_crystal_electrode_map
            
        for electrode in electrode_map:
            rena = electrode[0]
            channel = electrode[1]
            electrode_xyz = electrode[2:]
            
            xyz = crystal_xyz + electrode_xyz
            if use_crystal_z:
                xyz[2] = crystal_xyz[2]
            
            channel_map[channel_index, 0:4] = [node, board, rena, channel]
            channel_map[channel_index, 4:]  = xyz
            channel_index += 1
    
    fmt = ['%d', '%d', '%d', '%d'] + [f'%.{output_precision}f'] * 3
    np.savetxt(output_dir + '/' + output_file_name, channel_map, fmt=fmt)
    
    
    
    # --- Plotting --- #
    
    if plot_crystal_point_map:
        plotting.plot_crystal_point_map(panel_1_crystal_map.copy(), panel_2_crystal_map.copy())
    
    if plot_crystal_surface_map:
        plotting.plot_crystal_surface_map(panel_1_crystal_map.copy(), panel_2_crystal_map.copy(),
                                      crystal_x_width, crystal_y_width, crystal_z_width)
    
    
    if plot_electrode_point_map:
        plotting.plot_electrode_point_map(panel_1_top_crystal_electrode_map.copy(),
                                          panel_1_bottom_crystal_electrode_map.copy(),
                                          crystal_z_width, crystal_z_pitch)
    
    if plot_electrode_surface_map:
        plotting.plot_electrode_surface_map(panel_1_top_crystal_electrode_map.copy(),
                                            panel_1_bottom_crystal_electrode_map.copy(),
                                            crystal_x_width, crystal_y_width,
                                            crystal_z_width, crystal_z_pitch,
                                            anode_strip_width, cathode_strip_width)
    
    
    if plot_NodeBoard_channels:
        node_board_dictionary = mapping.build_NodeBoard_dict(channel_map)
        test_channels = []
        for NodeBoard in NodeBoard_plot_list:
            test_channels.append(node_board_dictionary[NodeBoard])
            
        test_channels = np.array(test_channels).reshape([channels_per_crystal*len(NodeBoard_plot_list), 7])   
        plotting.plot_test_channels(test_channels, panel_1_crystal_map.copy(), panel_2_crystal_map.copy(),
                               crystal_x_width, crystal_y_width, crystal_z_width)



if __name__ == '__main__':
    main()