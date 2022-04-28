# Other functions
from random import randint
import blessed, time
import socket

#Function for the game 

def setup(map_path, map_size, werewolf_dico, food_dico):
    """Creates the dictionnaries and the map size varAIbles.

    Parameters
    ----------
    map_path : the path to find the .ano file (str)
    map_size : the data base which countains the map size (list)
    werewolf_dico : the dictionnary which countains all of the wolves datas (dict)
    food_dico : the dictionnary that which countains all of the foods datas (dict)

    Returns
    -------
    map_size: the data base which countains the map size (list)
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)
    food_dico: the dictionnary that which countains all of the foods datas (dict)

    Version
    -------
    specification: Thomas Schobbens (v.3 06/03/2022)
    implementation: Thomas Schobbens (v.4 06/03/2022)

    """

    iteration = 0

    file = open(map_path, "r") # Open the .ano file
    file = (file.read()).split("\n") # Read the file and create a list which each index value is a line
    for line in file:
        iteration += 1 # Increase line N° to read
        line_text = line.split(" ")
        element_index = 0
        if iteration == 2: # For line N°2
            map_size.append(int(line_text[0]))
            map_size.append(int(line_text[1]))

        if iteration > 3 and iteration < 22: # For each line between line N°3 and line N°22
            line_text.insert(4, 100) # Add the energy varAIble for which the base value is 100 (0 <= Energy >= 100)
            line_text.insert(5, 0) # Add the attack buff varAIble for which the base value is 0 (0-10-20-30-40-50-60-70-80-90-100)
            line_text.insert(6, False) # Add the has_played varAIble for which the base value is False (False-True)
            werewolf_list = []
            for element in line_text:
                element_index += 1
                if element_index != 4:
                    werewolf_list.append(int(element)) # Turn all the elements of the list (except the string type) into an integral
                else:
                    werewolf_list.append(element) # Add the wolf type to the list
            werewolf_dico_key = str([werewolf_list[1],werewolf_list[2]])
            werewolf_dico[werewolf_dico_key] = [werewolf_list[0], werewolf_list[3], werewolf_list[4], werewolf_list[5], line_text[6]] # Add a key (x and y) to the dico with the werewolf datas

        if iteration > 22: # For each line after line N°22
            food_list = []
            for element in line_text:
                element_index += 1
                if element_index != 3: # Turn all the elements of the list (except the type) into an integral
                    food_list.append(int(element))
                else:
                    food_list.append(element) # Add the food type to the list
            food_dico_key = str([food_list[0], food_list[1]])
            food_dico[food_dico_key] = [food_list[2], food_list[3]] # Add a key (x and y) to the dico with the food datas
    
    return [map_size, werewolf_dico, food_dico]

def check_orders(order, list_to_append, list_str, map_size, werewolf_dico, group_1, group_2):
    """Appends the orders into the 4 different lists.
    
    Parameters
    ----------
    order: the order to check and to append (list)
    list_to_append: the list to which the order should be append (list)
    list_str: a text version of the list, only used to check for pacify list (str)
    map_size: the size of the map (list)
    werewolf_dico: the dictionnary for the werewolves (dict)
    group_1: group of player (int)
    group_2: group of player (int)

    Returns
    -------
    list_to_append: the list to which the order should be append (list)

    Version
    -------
    specification: Alexis Regardin (v.5 24/03/2022)
    implementation: Alexis Regardin (v.5 27/03/2022) 

    """
    origin = order[0].split("-")
    origin = [int(origin[0]), int(origin[1])]
 
    if list_str == "pacify_list": # If the order should be in the [pacify] list
        if (werewolf_dico[str(origin)][1]) == "omega" and (werewolf_dico[str(origin)][2]) >= 40: # Check if the square is an Omega and if the Omega has more than or exactly 40 energy
            list_to_append.append(origin) # Append the order to pacify_list
    else: # If the order should be in the [buff|eat|move] list
        target = order[1]
        target = target[1:].split("-")
        target = [int(target[0]), int(target[1])]
        x_difference = (target[0] - origin[0])
        y_difference = (target[1] - origin[1])
        total_difference = x_difference * y_difference # Multiplies the difference on x and on y, should be between -1 and 1 if 1 square away
        order = [origin, target]
        # Check if the origin exist in werewolf_dico, check if the target is 0 or 1 square away from the origin, check if the target is within the map area: higher or equal to 1 and smaller or equal to the map_size and if the wolf has at least 1 energy
        if total_difference in [-1,0,1] and target[0] >= 1 and target[1] >= 1 and target[0] <= map_size[0] and target[1] <= map_size[1] and x_difference in [-1,0,1] and y_difference in [-1,0,1]:
            if list_str == "buff_list":
                if (werewolf_dico[str(origin)][2]) > 0: # Humans can't attack
                    list_to_append.append(order) # Append the order to buff_list
            else: # list_str == "eat_list" or == "move_list"
                if (werewolf_dico[str(origin)][2])>= 0:
                    list_to_append.append(order) # Append the order to either eat_list or move_list

    return list_to_append

def read_orders(orders, pacify_list, buff_list, eat_list, move_list, map_size, werewolf_dico):
    """Checks if each separate order can be attributed to any of the 4 order types.

    Parameters
    -----------
    orders: the orders input (str)
    pacify_list: the list of pacify orders (list)
    buff_list: the list of buffs (list)
    eat_list: the list of eat orders (list)
    move_list: the list of move orders (list)
    map_size: the size of the map (list)
    werewolf_dico: the dictionnary for the werewolves (dict)

    Returns
    -------
    pacify_list: the list of pacify orders (list)
    buff_list: the list of buffs (list)
    eat_list: the list of eat orders (list)
    move_list: the list of move orders (list)

    Version
    -------
    specification: Thomas Schobbens (v.3 06/03/2022)
    implementation: Thomas Schobbens (v.4 07/03/2022)

    """
    try: # Check if the Order text contains any Errors
        for order in orders:
            order = order.split(":")
            if "Pacify" in order[1] and "*" not in order[1] and "@" not in order[1] and "<" not in order[1]:# Check if the Order text contains the Pacify requirements
                pacify_list = check_orders(order, pacify_list, "pacify_list", map_size, werewolf_dico, 1, 2)
                
            if "*" in order[1] and "Pacify" not in order[1] and "@" not in order[1] and "<" not in order[1]:# Check if the Order text contains the Attack requirements
                buff_list = check_orders(order, buff_list, "buff_list", map_size, werewolf_dico,1,2)

            if "<" in order[1] and "Pacify" not in order[1] and "*" not in order[1] and "@" not in order[1]:# Check if the Order text contains the Eat requirements
                eat_list = check_orders(order, eat_list, "eat_list", map_size, werewolf_dico,1,2)               

            if "@" in order[1] and "Pacify" not in order[1] and "*" not in order[1] and "<" not in order[1]:# Check if the Order text contains the Move requirements
                move_list = check_orders(order, move_list, "move_list", map_size, werewolf_dico,1,2)             

    except: # If the Order text contains any errors then the Order is skipped and not saved
        pass
    return [pacify_list, buff_list, eat_list, move_list]

def pacify_orders(order, werewolf_dico, buff_list):
    """Loops over the attacks of buff_list.
    For each of these values, check if the location is close enough from the Omega, if it does then remove it from the attack_list.

    Parameters
    ----------
    order: the pacify order to check (list)
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)
    buff_list: the list of buffs (list)

    Returns
    -------
    buff_list: the list of buffs (list)

    Version
    -------
    specification: Alexis Regardin (v.3 08/03/2022)
    implementation: Thomas Schobbens (v.3 06/03/2022)

    """
    
    print("Pacify at:", order)
    origin_loc = str(order)
    origin_wolf = werewolf_dico[origin_loc]
    origin_has_played = origin_wolf[4]

    if origin_has_played == False: # Check if the wolf have played this turn
        new_origin_energy = origin_wolf[2] - 40 # Decrease the Omega energy by 40
        new_origin_wolf = origin_wolf
        new_origin_wolf[2] = new_origin_energy
        new_origin_wolf[4] = True
        werewolf_dico[origin_loc] = new_origin_wolf # Update the Omega

        for attack in buff_list: # Loop over each pseudo legal attacks of this turn
            attack_origin = attack[0]
            x_difference = attack_origin[0] - order[0]
            y_difference = attack_origin[1] - order[1]

            if x_difference <= 6  and x_difference >= -6 and y_difference <= 6 and y_difference >= -6: # Check if the attack is at less than 6 squares from the Pacify
                buff_list.remove(attack)   
    return [buff_list, werewolf_dico]

def apply_buffs(order, werewolf_dico, attack_list, no_damage_turn):
    """Applies the buffs to the attacking wolves for this turn, legal attacks will be sent to the attack_list.

    Parameters
    ----------
    order: the buff order to check (list)
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)
    attack_list: the list of attacks for this turn (list) 

    Returns
    -------
    attack_list: the list of attacks for this turn (list) 

    Version
    -------
    specification: Alexis Regardin (v.4 08/03/2022)
    implementation: Thomas Schobbens (v.4 06/03/2022)

    """

    origin = order[0]
    
    origin_loc = str(order[0])
    target_loc = str(order[1])

    origin_wolf = werewolf_dico[origin_loc]
    origin_has_played = origin_wolf[4]
    origin_team = origin_wolf[0]

    target_wolf = werewolf_dico[target_loc]

    if target_wolf != None: # Target exists
        target_team = target_wolf[0]

        if origin_has_played == False:

            if origin_team != target_team: # Check if the Origin Wolf and the Target Wolf are in different teams, also check if the wolf tries to attack it's own square
                bonus_amount = 0

                origin_x = origin[0]
                origin_y = origin[1]

                modified_werewolf_dico = werewolf_dico
                del modified_werewolf_dico[origin_loc] # The wolf doesn't give a buff to itself
                for wolves in modified_werewolf_dico: # Loop over all the wolves to apply the attack bonus on the origin wolf
                    if origin_team == modified_werewolf_dico[wolves][0]: # Check for each wolf which is in the same team as the attacker origin wolf
                        wolves_list = wolves[1:-1]
                        bonus_list = wolves_list.split(", ")
                        bonus_x = int(bonus_list[0])
                        bonus_y = int(bonus_list[1])
                        x_difference = origin_x - bonus_x
                        y_difference = origin_y - bonus_y

                        if modified_werewolf_dico[wolves][1] == "normal" or modified_werewolf_dico[wolves][0] == "omega":
                            if x_difference <= 2 and x_difference >= -2 and y_difference <= 2 and y_difference >= -2: # Normal or Omega wolf is close enough to give a buff
                                bonus_amount += 10

                        elif modified_werewolf_dico[wolves][1] == "alpha":
                            if x_difference <= 4 and x_difference >= -4 and y_difference <= 4 and y_difference >= -4: # Alpha wolf is close enough to give a buff
                                bonus_amount += 30

                wolf_with_buff = origin_wolf
                wolf_with_buff[3] = bonus_amount
                wolf_with_buff[4] = True
                werewolf_dico[origin_loc] = wolf_with_buff
                print(origin_loc, origin_wolf, "attacks", target_loc, target_wolf)
                attack_list.append(order)
                return [attack_list, werewolf_dico, 0]

    else:
        return [attack_list, werewolf_dico, no_damage_turn]

def attack_orders(order, werewolf_dico):
    """Applies the damage to the target wolves.
    All of the orders in here are legal, the origin is an alive wolf which hasn't played and which aim for a wolf of the opposite team at 1 square range from itself.

    Parameters
    ----------
    order: the attack order to check (list)
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)

    Returns
    -------
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)

    Version
    -------
    specification: Alexis Regardin (v.4 08/03/2022)
    implementation: Thomas Schobbens (v.3 06/03/2022)

    """
    
    origin_loc = str(order[0])
    target_loc = str(order[1])

    origin_wolf = werewolf_dico[origin_loc]
    target_wolf = werewolf_dico[target_loc]
    
    energy_left = target_wolf[2] - (int(origin_wolf[2]/10) + int(round(origin_wolf[3]/10))) # Energy left = victim energy - (10% rounded down of attacker energy + 10% rounded down attacker attack buff)
    if energy_left < 0: # Energy can't drop under 0
        energy_left = 0
    
    new_target_wolf = target_wolf
    new_target_wolf[2] = energy_left
    werewolf_dico[target_loc] = new_target_wolf # Update the victim wolf energy

    return werewolf_dico

def eat_orders(order, werewolf_dico, food_dico):
    """Allows wolves to eat food, it modifies the dictionnaries and deletes the finished food from the food dictionnary.

    Parameters
    ----------
    order: the eat order to check (list)
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)
    food_dico: the dictionnary that which countains all of the foods datas (dict)

    Returns
    -------
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)
    food_dico: the dictionnary that which countains all of the foods datas (dict)

    Version
    -------
    specification: Alexis Regardin (v.4 08/03/2022)
    implementation: Thomas Schobbens (v.3 06/03/2022)

    """
    
    target_loc = str(order[1])

    if target_loc in food_dico: # Check if the food location exist in the food dictonnary
        origin_loc = str(order[0])
        origin_wolf = werewolf_dico[origin_loc]
        origin_has_played = origin_wolf[4]

        if origin_has_played == False: # Check if the wolf have played this turn
            origin_energy = origin_wolf[2]

            if origin_energy != 100: # Check if the wolf doesn't have full Energy
                target_food = food_dico[target_loc]
                target_energy = target_food[1]
                print(origin_loc, origin_wolf, "eat", target_loc, target_food)

                max_energy = 100 - origin_energy # Amount of energy that the wolf should eat to reach 100 Energy

                if target_energy <= max_energy: # The food doesn't have enough energy to feed the wolf to its maximum energy
                    wolf_new_energy = origin_energy + target_energy
                    werewolf_dico[origin_loc] = [origin_wolf[0], origin_wolf[1], wolf_new_energy, origin_wolf[3], True] # Update the wolf
                    del food_dico[target_loc] # The food is out of energy, delete it

                else: # The food has enough energy to feed the wolf to its maximum energy
                    food_energy_left = target_energy - max_energy
                    food_dico[target_loc] = [target_food[0], target_food[1], food_energy_left] # Update the food

                    wolf_new_energy = origin_energy + max_energy
                    werewolf_dico[origin_loc] = [origin_wolf[0], origin_wolf[1], wolf_new_energy, origin_wolf[3], True] # Update the wolf

    return [werewolf_dico, food_dico]

def move_orders(order, werewolf_dico):
    """Allows wolves and humans to move if the square is free, the order of orders is important here.

    Parameters
    ----------
    order: the move order to check (list)
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)

    Returns
    -------
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)

    Version
    -------
    specification: Alexis Regardin (v.4 08/03/2022)
    implementation: Thomas Schobbens (v.3 06/03/2022)

    """
    
    origin_loc = str(order[0])
    move_target = str(order[1])

    if origin_loc in werewolf_dico:
        origin_wolf = werewolf_dico[origin_loc]
        origin_has_played = origin_wolf[4]

        if origin_has_played == False and origin_wolf != None: # Check if the wolf have played this turn
            if move_target not in werewolf_dico: # Check if there is no wolf on the target square
                new_origin_wolf = origin_wolf
                print(origin_loc, "moves to", order[1])
                new_origin_wolf[4] = True
                werewolf_dico[move_target] = new_origin_wolf
                del werewolf_dico[origin_loc]

    return werewolf_dico

def apply_orders(pacify_list, buff_list, attack_list, eat_list, move_list, werewolf_dico, food_dico, no_damage_turn):
    """Apply all of the 4 different orders to the game.

    Parameters
    ----------
    pacify_list: all of the pacify orders (list)
    buff_list: all the possible attack orders (list)
    attack_list: the list of attacks for this turn (list) 
    eat_list: all of the eat orders (list)
    move_list: all of the move orders (list)
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)
    food_dico: the dictionnary that which countains all of the foods datas (dict)
    no_damage_turn: the amount of turn without dealing any damage (int)

    Returns
    -------
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)
    food_dico: the dictionnary that which countains all of the foods datas (dict)
    no_damage_turn: the amount of turn without dealing any damage (int)

    Version
    -------
    specification: Thomas Schobbens (v.2 06/03/2022)
    implementation: Thomas Schobbens (v.2 06/03/2022)

    """

    for order in pacify_list:
        pacify_orders_var = pacify_orders(order, werewolf_dico, buff_list)
        buff_list = pacify_orders_var[0]
        werewolf_dico = pacify_orders_var[1]

    for order in buff_list:
        var_apply_buffs = apply_buffs(order, werewolf_dico, attack_list, no_damage_turn)  
        try:
            attack_list = var_apply_buffs[0]
            werewolf_dico = var_apply_buffs[1]
            no_damage_turn = var_apply_buffs[2]
        except:
           pass 

    for order in attack_list:
        werewolf_dico = attack_orders(order, werewolf_dico)        

    for order in eat_list:
        eat_orders_var = eat_orders(order, werewolf_dico, food_dico)
        werewolf_dico = eat_orders_var[0]
        food_dico = eat_orders_var[1]

    for order in move_list:
        werewolf_dico = move_orders(order, werewolf_dico)
    
    return [werewolf_dico, food_dico, no_damage_turn]

#Functions for remote

def create_server_socket(local_port, verbose):
    """Creates a server socket.
    
    Parameters
    ----------
    local_port: port to listen to (int)
    verbose: True if verbose (bool)
    
    Returns
    -------
    socket_in: server socket (socket.socket)
    
    """
    
    socket_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_in.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # deal with a socket in TIME_WAIT state

    if verbose:
        print(' binding on local port %d to accept a remote connection' % local_port)
    
    try:
        socket_in.bind(('', local_port))
    except:
        raise IOError('local port %d already in use by your group or the referee' % local_port)
    socket_in.listen(1)
    
    if verbose:
        print('   done -> can now accept a remote connection on local port %d\n' % local_port)
        
    return socket_in

def create_client_socket(remote_IP, remote_port, verbose):
    """Creates a client socket.
    
    Parameters
    ----------
    remote_IP: IP address to send to (int)
    remote_port: port to send to (int)
    verbose: True if verbose (bool)
    
    Returns
    -------
    socket_out: client socket (socket.socket)
    
    """

    socket_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_out.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # deal with a socket in TIME_WAIT state
    
    connected = False
    msg_shown = False
    
    while not connected:
        try:
            if verbose and not msg_shown:
                print(' connecting on %s:%d to send orders' % (remote_IP, remote_port))
                
            socket_out.connect((remote_IP, remote_port))
            connected = True
            
            if verbose:
                print('   done -> can now send orders to %s:%d\n' % (remote_IP, remote_port))
        except:
            if verbose and not msg_shown:
                print('   connection failed -> will try again every 100 msec...')
                
            time.sleep(.1)
            msg_shown = True
            
    return socket_out
       
def wait_for_connection(socket_in, verbose):
    """Waits for a connection on a server socket.
    
    Parameters
    ----------
    socket_in: server socket (socket.socket)
    verbose: True if verbose (bool)
    
    Returns
    -------
    socket_in: accepted connection (socket.socket)
    
    """
    
    if verbose:
        print(' waiting for a remote connection to receive orders')
        
    socket_in, remote_address = socket_in.accept()
    
    if verbose:
        print('   done -> can now receive remote orders from %s:%d\n' % remote_address)
        
    return socket_in            

def create_connection(your_group, other_group=0, other_IP='127.0.0.1', verbose=False):
    """Creates a connection with a referee or another group.
    
    Parameters
    ----------
    your_group: id of your group (int)
    other_group: id of the other group, if there is no referee (int, optional)
    other_IP: IP address where the referee or the other group is (str, optional)
    verbose: True only if connection progress must be displayed (bool, optional)
    
    Returns
    -------
    connection: socket(s) to receive/send orders (dict of socket.socket)
    
    Raises
    ------
    IOError: if your group fails to create a connection
    
    Notes
    -----
    Creating a connection can take a few seconds (it must be initAIlised on both sides).
    
    If there is a referee, leave other_group=0, otherwise other_IP is the id of the other group.
    
    If the referee or the other group is on the same computer than you, leave other_IP='127.0.0.1',
    otherwise other_IP is the IP address of the computer where the referee or the other group is.
    
    The returned connection can be used directly with other functions in this module.
            
    """
    
    # init verbose display
    if verbose:
        print('\n[--- starts connection -----------------------------------------------------\n')
        
    # check whether there is a referee
    if other_group == 0:
        if verbose:
            print('** group %d connecting to referee on %s **\n' % (your_group, other_IP))
        
        # create one socket (client only)
        socket_out = create_client_socket(other_IP, 42000+your_group, verbose)
        
        connection = {'in':socket_out, 'out':socket_out}
        
        if verbose:
            print('** group %d successfully connected to referee on %s **\n' % (your_group, other_IP))
    else:
        if verbose:
            print('** group %d connecting to group %d on %s **\n' % (your_group, other_group, other_IP))

        # create two sockets (server and client)
        socket_in = create_server_socket(42000+your_group, verbose)
        socket_out = create_client_socket(other_IP, 42000+other_group, verbose)
        
        socket_in = wait_for_connection(socket_in, verbose)
        
        connection = {'in':socket_in, 'out':socket_out}

        if verbose:
            print('** group %d successfully connected to group %d on %s **\n' % (your_group, other_group, other_IP))
        
    # end verbose display
    if verbose:
        print('----------------------------------------------------- connection started ---]\n')

    return connection

def bind_referee(group_1, group_2, verbose=False):
    """Put a referee between two groups.
    
    Parameters
    ----------
    group_1: id of the first group (int)
    group_2: id of the second group (int)
    verbose: True only if connection progress must be displayed (bool, optional)
    
    Returns
    -------
    connections: sockets to receive/send orders from both players (dict)
    
    Raises
    ------
    IOError: if the referee fails to create a connection
    
    Notes
    -----
    Putting the referee in place can take a few seconds (it must be connect to both groups).
        
    connections contains two connections (dict of socket.socket) which can be used directly
    with other functions in this module.  connection of first (second) player has key 1 (2).
            
    """
    
    # init verbose display
    if verbose:
        print('\n[--- starts connection -----------------------------------------------------\n')

    # create a server socket (first group)
    if verbose:
        print('** referee connecting to first group %d **\n' % group_1)        

    socket_in_1 = create_server_socket(42000+group_1, verbose)
    socket_in_1 = wait_for_connection(socket_in_1, verbose)

    if verbose:
        print('** referee succcessfully connected to first group %d **\n' % group_1)        
        
    # create a server socket (second group)
    if verbose:
        print('** referee connecting to second group %d **\n' % group_2)        

    socket_in_2 = create_server_socket(42000+group_2, verbose)
    socket_in_2 = wait_for_connection(socket_in_2, verbose)

    if verbose:
        print('** referee succcessfully connected to second group %d **\n' % group_2)        
    
    # end verbose display
    if verbose:
        print('----------------------------------------------------- connection started ---]\n')

    return {1:{'in':socket_in_1, 'out':socket_in_1},
            2:{'in':socket_in_2, 'out':socket_in_2}}

def close_connection(connection):
    """Closes a connection with a referee or another group.
    
    Parameters
    ----------
    connection: socket(s) to receive/send orders (dict of socket.socket)
    
    """
    
    # get sockets
    socket_in = connection['in']
    socket_out = connection['out']
    
    # shutdown sockets
    socket_in.shutdown(socket.SHUT_RDWR)    
    socket_out.shutdown(socket.SHUT_RDWR)
    
    # close sockets
    socket_in.close()
    socket_out.close()

def notify_remote_orders(connection, orders):
    """Notifies orders to a remote player.
    
    Parameters
    ----------
    connection: sockets to receive/send orders (dict of socket.socket)
    orders: orders to notify (str)
        
    Raises
    ------
    IOError: if remote player cannot be reached
    
    """

    # deal with null orders (empty string)
    if orders == '':
        orders = 'null'
    
    # send orders
    try:
        connection['out'].sendall(orders.encode())
    except:
        raise IOError('remote player cannot be reached')

def get_remote_orders(connection):
    """Returns orders from a remote player.

    Parameters
    ----------
    connection: sockets to receive/send orders (dict of socket.socket)
        
    Returns
    ----------
    player_orders: orders given by remote player (str)

    Raises
    ------
    IOError: if remote player cannot be reached
            
    """
   
    # receive orders    
    try:
        orders = connection['in'].recv(65536).decode()
    except:
        raise IOError('remote player cannot be reached')
        
    # deal with null orders
    if orders == 'null':
        orders = ''
        
    return orders

#Blessed

term = blessed.Terminal()

def terminal_display(map_size, total_turn, no_damage_turn, werewolf_dico, food_dico):
    """
    Create and print the map to play.

    Parameters :
    ------------
    map_size : the data base which countains the map size (list)
    total_turn : number of turn since the beginning of the game (int)
    no_dammage_turn : number of turn since no wolves were damaged (int)
    werewolf_dico : the dictionnary which countains all of the wolves datas (dict)

    Version :
    ---------
    specification : Gautier Hisette (v.2 25/03/2022)
    implementation : Gautier Hisette (v.3 25/03/2022)

    """

    print(term.clear)

    map_size_y = map_size [0] * 2 + 1
    map_size_x = map_size [1] * 4 + 1
    
    for row in range (0, map_size_y):
        pass

        for col in range (0, map_size_x):
            pass

            if row == 0 and col == 0:
                unicode_symbol = "┌"

            elif row == 0 and col == map_size_x - 1:
                unicode_symbol = "┐"

            elif row == 0 and col % 4 == 0:
                unicode_symbol = "┬"

            elif row == map_size_y - 1 and col == 0:
                unicode_symbol = "└"

            elif row == map_size_y - 1 and col == map_size_x - 1:
                unicode_symbol = "┘"

            elif row == map_size_y - 1 and col % 4 == 0:
                unicode_symbol = "┴"

            elif row % 2 == 0 and col == 0:
                unicode_symbol = "├"

            elif row % 2 == 0 and col == map_size_x - 1:
                unicode_symbol = "┤"

            elif row % 2 != 0 and col % 4 == 0:
                unicode_symbol = "│"

            elif row % 2 == 0 and col % 4 != 0: 
                unicode_symbol = "─"

            elif row % 2 == 0 and col % 4 == 0:
                unicode_symbol = "┼"
            
            else:
                unicode_symbol = " "

            print(term.move_xy(col, row) + term.on_black + unicode_symbol + term.normal, end='', flush=True)

    y_shift = -1 # Shift on  to display the health and energy of the werewolves and foods on the side of the board

    for food in food_dico: # /!\ à la fin de eat order garder les ordres légaux dans une liste pour modifier l'affichage des foods : origin -> target
        y_shift += 1
        food_type = food_dico[str(food)][0]
        if len(food_dico[str(food)]) == 2:
            food_energy = food_dico[str(food)][1]
        else:
            food_energy = food_dico[str(food)][2]

        if food_energy > 0:
            if food_type == "berries":
                max_food_energy = 10
            elif food_type == "apples":
                max_food_energy = 30
            elif food_type == "mice":
                max_food_energy = 50
            elif food_type == "rabbits":
                max_food_energy = 100
            elif food_type == "deers":
                max_food_energy = 500
            else:
                max_food_energy = 1

            food_percent = int(food_energy / max_food_energy * 10)
            food_unicode_repeat = " 🗲" * food_percent + "  <-> "

            print(term.move_xy(map_size[1] * 4 + 10, y_shift) + term.gold + food + " : " + food_unicode_repeat + str(food_energy) + term.normal, end='', flush=True)  
            
            food = food[1:-1].split(',')
            print(term.move_xy((int(food[0]) * 4) -2, (int(food[1]) * 2 ) - 1) + term.on_black + term.gold + '𝛟' + term.normal, end='', flush=True)

    y_shift += 4

    alpha_y = y_shift
    omega_y = y_shift + 2

    y_shift += 2

    for wolf in werewolf_dico: # /!\ à la fin de move order garder les ordres légaux dans une liste pour modifier l'affichage des loups : origin -> target
        wolf_loc = wolf[1:-1].split(',')
        if werewolf_dico[str(wolf)][0] == 1:
            wolf_percent =  int(werewolf_dico[str(wolf)][2]/ 10)
            wolf_unicode_repeat = " ❤" * wolf_percent + "  <-> "

            if werewolf_dico[str(wolf)][2] > 0:
                if werewolf_dico[str(wolf)][1] == 'alpha':
                    unicode_symbol = "𝞪"
                    print(term.move_xy(map_size[1] * 4 + 10, alpha_y) + term.aqua + "𝞪 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)

                elif werewolf_dico[str(wolf)][1] == 'omega':
                    unicode_symbol = "𝛀"
                    print(term.move_xy(map_size[1] * 4 + 10, omega_y) + term.aqua + "𝛀 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)

                else:
                    y_shift += 2
                    unicode_symbol = "𝞈"
                    print(term.move_xy(map_size[1] * 4 + 10, y_shift) + term.aqua + "𝞈 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)

            elif werewolf_dico[str(wolf)][2] == 0:
                if werewolf_dico[str(wolf)][1] == 'alpha':
                    unicode_symbol = "𝞪"
                    print(term.move_xy(map_size[1] * 4 + 10, alpha_y) + term.deepskyblue4 + "𝞪 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)

                elif werewolf_dico[str(wolf)][1] == 'omega':
                    unicode_symbol = "𝛀"
                    print(term.move_xy(map_size[1] * 4 + 10, omega_y) + term.deepskyblue4 + "𝛀 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)

                else:
                    y_shift += 2
                    unicode_symbol = "𝞈"
                    print(term.move_xy(map_size[1] * 4 + 10, y_shift) + term.deepskyblue4 + "𝞈 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)
            
            if werewolf_dico[str(wolf)][2] > 0:
                print(term.move_xy((int(wolf_loc[0]) * 4) - 2, (int(wolf_loc[1])*2) - 1) + term.on_black + term.aqua + unicode_symbol + term.normal, end='', flush=True)

            elif werewolf_dico[str(wolf)][2] == 0:
                print(term.move_xy((int(wolf_loc[0]) * 4) - 2, (int(wolf_loc[1])*2) - 1) + term.on_black + term.deepskyblue4 + unicode_symbol + term.normal, end='', flush=True)

    y_shift -= 14

    for wolf in werewolf_dico: # /!\ à la fin de move order garder les ordres légaux dans une liste pour modifier l'affichage des loups : origin -> target
        wolf_loc = wolf[1:-1].split(',')
        if werewolf_dico[str(wolf)][0] == 2:
            wolf_percent =  int(werewolf_dico[str(wolf)][2]/ 10)
            wolf_unicode_repeat = " ❤" * wolf_percent + "  <-> "

            if werewolf_dico[str(wolf)][2] > 0:
                if werewolf_dico[str(wolf)][1] == 'alpha':
                    unicode_symbol = "𝞪"
                    print(term.move_xy(map_size[1] * 4 + 60, alpha_y) + term.greenyellow + "𝞪 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)

                elif werewolf_dico[str(wolf)][1] == 'omega':
                    unicode_symbol = "𝛀"
                    print(term.move_xy(map_size[1] * 4 + 60, omega_y) + term.greenyellow + "𝛀 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)

                else:
                    unicode_symbol = "𝞈"
                    y_shift += 2
                    print(term.move_xy(map_size[1] * 4 + 60, y_shift) + term.greenyellow + "𝞈 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)

            elif werewolf_dico[str(wolf)][2] == 0:
                if werewolf_dico[str(wolf)][1] == 'alpha':
                    unicode_symbol = "𝞪"
                    print(term.move_xy(map_size[1] * 4 + 60, alpha_y) + term.forestgreen + "𝞪 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)

                elif werewolf_dico[str(wolf)][1] == 'omega':
                    unicode_symbol = "𝛀"
                    print(term.move_xy(map_size[1] * 4 + 60, omega_y) + term.forestgreen + "𝛀 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)

                else:
                    unicode_symbol = "𝞈"
                    y_shift += 2
                    print(term.move_xy(map_size[1] * 4 + 60, y_shift) + term.forestgreen + "𝞈 " + wolf + " : " + wolf_unicode_repeat + str(werewolf_dico[str(wolf)][2]) + term.normal, end='', flush=True)


            if werewolf_dico[str(wolf)][2] > 0:
                print(term.move_xy((int(wolf_loc[0]) * 4) - 2, (int(wolf_loc[1])*2) - 1) + term.on_black + term.greenyellow + unicode_symbol + term.normal, end='', flush=True)

            elif werewolf_dico[str(wolf)][2] == 0:
                print(term.move_xy((int(wolf_loc[0]) * 4) - 2, (int(wolf_loc[1])*2) - 1) + term.on_black + term.forestgreen + unicode_symbol + term.normal, end='', flush=True)



    y_shift += 4
    print(term.move_xy(map_size[1] * 4 + 10, y_shift) + term.magenta + "⌛ Turns: " + str(total_turn) + term.normal, end='', flush=True)
    y_shift += 1
    print(term.move_xy(map_size[1] * 4 + 10, y_shift) + term.magenta + "⏰ Turns without damage: " + str(no_damage_turn) + term.normal, end='', flush=True)

    for x in range(1, map_size[1] + 1):
        print(term.move_xy((x+1) * 4 - 6, map_size[0] * 2 + 1) + term.maroon1 + str(x) + term.normal, end='', flush=True)

    for y in range(1, map_size[0] + 1):
        print(term.move_xy(map_size[1] * 4 + 2, (y+1) * 2 - 3) + term.maroon1 + str(y) + term.normal, end='', flush=True)

#Functions for the AI

def splitter(location):
    """
    Transform a string of coordinate [x,y] into a list of 2 elements

    Parameters :
    ------------
    location : coordinate of an element (str)

    Return :
    --------
    location : 2 elements ['x','y'] (list)

    Versions :
    ----------
    specification : Alexis Regardin (v.2 22/04/2022)
    implementation : Alexis Regardin (v.2 22/04/2022)
    
    """
    location = (location.strip('[',))
    location = location.strip(']')
    location = location.split(',')

    return location

def differences(location, x_origin,y_origin):
    """
    Compute the difference between the location of a wolf and its target

    Parameters :
    ------------
    location : coordinate of an element (list)
    x_origin : x coordinate of a wolf (int)
    y_origin : y coordinate of a wolf (int)
    Returns :
    ---------
    x_difference : the difference in distance on the x-axis between the origin and its target (int)
    y_difference : the difference in distance on the y-axis between the origin and its target (int)

    Versions : 
    ----------
    specification : Alexis Regardin (v.1 27/04/2022)
    implementation : Alexis Regardin (v.1 27/04/2022)
    """
    x_position_target = int(location[0])
    y_position_target = int(location[1])
    x_difference = x_position_target - x_origin
    y_difference = y_position_target - y_origin

    return [x_difference, y_difference]
#Utiliser dans check orders
def AI_attack(x_position_origin, y_position_origin, x_position_target, y_position_target):
    """
    Attacks of the AI

    Paramters :
    ----------- 
    x_position_origin : position on the x-axis of the attacking wolf (int) 
    y_position_origin : position on the y-axis of the attacking wolf (int)
    x_position_target : position on the x-axis of the attacked wolf (int)
    y_position_target : position on the y-axis of the attacked wolf (int)

    Returns :
    ---------
    order_turn : one order of attack for this turn (str)

    Versions :
    ----------
    specification : Alexis Regardin (v.1 27/04/2022)
    implementation : Alexis Regardin (v.1 27/04/2022)
    
    """
    origin_position = str(x_position_origin) + '-' + str(y_position_origin)
    target_position = str(x_position_target) + '-' + str(y_position_target) 
    order_turn = (origin_position + ':*' + target_position) #Create an attack order like this : x-y:*x-y

    return order_turn

#AI

def AI(werewolf_dico, food_dico, team):
    """
    Final AI

    Parameters
    ----------
    werewolf_dico: the dictionnary which countains all of the wolves datas (dict)
    food_dico: the dictionnary that which countains all of the foods datas (dict)
    team: team for the AI (int)

    Returns
    -------
    orders: orders given for one turn (str)

    Versions
    --------
    specification : Alexis Regardin (v.2 22/04/2022)
    implementation : Alexis Regardin (v.4 27/04/2022)
    """

    orders = ''
    AI_wolves = []
    enemy_wolves = []


    for location in werewolf_dico: #Create a list of all the wolves of the AI's team
        if werewolf_dico[location][0] == team:
                AI_wolves.append(location) 

    for location in werewolf_dico: #Create a list of all the wolves of the enemy
        if werewolf_dico[location][0] != team:
            enemy_wolves.append(location)
    
    
    for AI_location in AI_wolves:
        if werewolf_dico[AI_location][1] == 'omega':
            omega_location = splitter(AI_location)
            x_position_origin = int(omega_location[0])
            y_position_origin = int(omega_location[1])

            for wolves in enemy_wolves:
                location = splitter(wolves)
                result = differences(location, x_position_origin,y_position_origin) 
                if result[0] in range(-6,6) and result[1] in range(-6,6): #The omega wont become an human and there is an enemy in the area
                    if werewolf_dico[AI_location][2] > 40:
                        origin_position = str(x_position_origin) + '-' + str(y_position_origin) #Create something we can use for the order : x-y 
                        pacify_order = (origin_position + ':Pacify')
                        orders += (pacify_order + ' ')


    for wolves in AI_wolves:
        wolves_coordinate = splitter(wolves)
        x_position_origin = int(wolves_coordinate[0])
        y_position_origin = int(wolves_coordinate[1]) #Keep the x and y coordinate of the wolf from the AI's team

        for enemy in enemy_wolves:
            coordinate = splitter(enemy)
            x_position_target = int(coordinate[0])
            y_position_target = int(coordinate[1])
            x_difference = x_position_target - x_position_origin
            y_difference = y_position_target - y_position_origin
            total_difference = x_difference * y_difference

            if werewolf_dico[wolves][2] <= 10: #The wolf has few energy left, there is still food left, send him to the nearest food
                for food in food_dico:
                    food = splitter(food)
                    x_position_target = int(food[0])
                    y_position_target = int(food[1])
                    x_difference = x_position_target - x_position_origin
                    y_difference = y_position_target - y_position_origin
                    total_difference = x_difference * y_difference
                    if total_difference in [-1,0,1] and (x_position_target - x_position_origin) in [-1,0,1] and (y_position_target - y_position_origin)  in [-1,0,1]: #Check if the target is 0 or 1 square away from the origin
                        origin_position = str(x_position_origin) + '-' + str(y_position_origin)
                        target_position = str(x_position_target) + '-' + str(y_position_target) 
                        order_turn = (origin_position + ':<' + target_position) #Create a eat order like this : x-y:<x-y 
                        orders += (order_turn + ' ')
                    else:
                        if (x_difference not in range(-1,1)) or (y_difference not in range(-1,1)): #The wolf isn't next to the food
                            if x_difference < -1:
                                x_position_moving = x_position_origin - 1
                            elif x_difference > 1:
                                x_position_moving = x_position_origin + 1
                            if y_difference < -1:
                                y_position_moving = y_position_origin - 1
                            elif y_difference > 1:
                                y_position_moving = y_position_origin + 1
        
                            order_turn = (str(x_position_origin) + '-' + str(y_position_origin) + ':@' + str(x_position_moving) + '-' + str(y_position_moving))
                            orders += (order_turn + ' ')
            
            if werewolf_dico[enemy][1] == 'alpha':
                if total_difference in [-1,0,1] and (x_position_target - x_position_origin) in [-1,0,1] and (y_position_target - y_position_origin) in [-1,0,1]: #Check if the target is 0 or 1 square away from the origin 
                    if werewolf_dico[wolves][2] > 10: #If the wolf has enough energy left to fight
                        order_turn = AI_attack(x_position_origin, y_position_origin, x_position_target, y_position_target) #Create an attack order like this : x-y:*x-y 
                        orders += (order_turn + ' ') #Add the order        

            if werewolf_dico[enemy][2] > 0:
                if total_difference in [-1,0,1] and (x_position_target - x_position_origin) in [-1,0,1] and (y_position_target - y_position_origin) in [-1,0,1]: #Check if the target is 0 or 1 square away from the origin 
                    if werewolf_dico[wolves][2] > 10: #If the wolf has enough energy left to fight
                        order_turn = AI_attack(x_position_origin, y_position_origin, x_position_target, y_position_target) #Create an attack order like this : x-y:*x-y 
                        orders += (order_turn + ' ') #Add the order 

            if (x_difference not in range(-1,1)) or (y_difference not in range(-1,1)): #The wolf isn't next to the alpha
                if (x_difference not in range(-1,1)) or (y_difference not in range(-1,1)): #The wolf isn't next to the food    
                    if x_difference < -1:
                        x_position_moving = x_position_origin - 1
                    elif x_difference > 1:
                        x_position_moving = x_position_origin + 1
                    if y_difference < -1:
                        y_position_moving = y_position_origin - 1
                    elif y_difference > 1:
                        y_position_moving = y_position_origin + 1
        
                    order_turn = (str(x_position_origin) + '-' + str(y_position_origin) + ':@' + str(x_position_moving) + '-' + str(y_position_moving))
                    orders += (order_turn + ' ')
                    
                                
    orders = str(orders)
    return orders

#Main function

def play_game(map_path, group_1, type_1, group_2, type_2):
    """Play a game.
    
    Parameters
    ----------
    map_path: path of map file (str)
    group_1: group of player 1 (int)
    type_1: type of player 1 (str)
    group_2: group of player (int)
    type_2: type of player 2 (str)
    
    Versions :
    ----------
    specification : Thomas Schobbens (v.2 07/03/2022)
    implementation : Alexis Regardin (v.4 24/03/2022)

    Notes :
    -------
    Player type is either 'human', 'AI' or 'remote'.
    
    If there is an external referee, set group id to 0 for remote player.
    
    """
    if type_1 == 'Remote' or type_2 == 'Remote':
        connection = create_connection(11,0)

    total_turn = 0
    no_damage_turn = 0
    team_1_alpha_energy = 100
    team_2_alpha_energy = 100

    map_size = []
    werewolf_dico = {}
    food_dico = {}

    setup_var = setup(map_path, map_size, werewolf_dico, food_dico)
    map_size = setup_var[0]
    werewolf_dico = setup_var[1]
    food_dico = setup_var[2]


    #while both alpha are alive or less than 200 turn without damage:
    while team_1_alpha_energy > 0 and team_2_alpha_energy > 0 and no_damage_turn < 200:
        total_turn += 1
        pacify_list = []
        buff_list = []
        attack_list = []
        eat_list = []
        move_list = []
        reset_werewolf_dico = {}
        for wolf in werewolf_dico: # Set all the has_played varAIbles to False
            reset = werewolf_dico[wolf]
            reset[4] = False
            reset_werewolf_dico[str(wolf)] = reset
        werewolf_dico = reset_werewolf_dico

        no_damage_turn += 1

        terminal_display(map_size, total_turn, no_damage_turn, werewolf_dico, food_dico)
        time.sleep(2)
        
        orders = []

        if type_1 == 'Player':
           Player1_orders = input("Quelles sont vos ordres pour l'équipe 1 ? ")
           Player1_orders = Player1_orders.split(" ")
           for order_to_add in Player1_orders:
                try:
                    orders.append(order_to_add)
                except:
                    pass
        elif type_1 == 'Remote':
            orders = get_remote_orders(connection) #Get the order from the connection

        if type_2 == 'Player':
            Player2_orders = input("Quelles sont vos ordres pour l'équipe 2 ? ")
            Player2_orders = Player2_orders.split(" ")
            for order_to_add in Player2_orders:
                try:
                    orders.append(order_to_add)
                except:
                    pass
        elif type_2 == 'Remote':
            orders = get_remote_orders(connection)
        
        try:
            if type_1 == 'AI':
                AI_orders = AI(werewolf_dico, food_dico, group_1)
                AI_orders = AI_orders.split(" ")
            
                del AI_orders[-1]
                for order_to_add in AI_orders:
                    try:
                        orders.append(order_to_add)
                    except:
                        pass
            if type_2 =='AI':
                AI_orders = AI(werewolf_dico, food_dico, group_2)
                AI_orders = AI_orders.split(" ")
            
                del AI_orders[-1]
                for order_to_add in AI_orders:
                    try:
                        orders.append(order_to_add)
                    except:
                        pass
        except:
            pass
        read_orders_var = read_orders(orders, pacify_list, buff_list, eat_list, move_list, map_size, werewolf_dico)
        pacify_list = read_orders_var[0]
        buff_list = read_orders_var[1]
        eat_list = read_orders_var[2]
        move_list = read_orders_var[3]
        apply_orders_var = apply_orders(pacify_list, buff_list, attack_list, eat_list, move_list, werewolf_dico, food_dico, no_damage_turn)
        werewolf_dico = apply_orders_var[0]
        food_dico = apply_orders_var[1]
        no_damage_turn = apply_orders_var[2]

        if type_1 == 'Remote' or type_2 == 'Remote':
            notify_remote_orders(connection,orders) #notify the other player

        for check_alpha in werewolf_dico:
            if werewolf_dico[check_alpha][1] == "alpha":
                if werewolf_dico[check_alpha][0] == 1:
                    team_1_alpha_energy = werewolf_dico[check_alpha][2]
                else:
                    team_2_alpha_energy = werewolf_dico[check_alpha][2]
        
    
    # End of the loop and of the game
    print('Total turns is ', total_turn)
    if type_1 == 'Remote' or type_2 == 'Remote':
        close_connection(connection)
    return [team_1_alpha_energy, team_2_alpha_energy, no_damage_turn, werewolf_dico]

alpha_energies = play_game("Map.ano",1, "AI",2, "AI")

if alpha_energies[0] == 0 and alpha_energies[1] == 0:
    print("Draw, both alpha are dead")
elif alpha_energies[0] == 0:
    print("Team 2 wins")
elif alpha_energies[1] == 0:
    print("Team 1 wins")
elif alpha_energies[2] == 200:
    energy_difference = 0
    for wolves in alpha_energies[3]:
        current_wolf = alpha_energies[3][wolves]
        if current_wolf [0] == 1:
            energy_difference += current_wolf[2]
        else:
            energy_difference -= current_wolf[2]
    print("Time Over")
    if energy_difference > 0:
        print("Team 1 win")
    elif energy_difference < 0:
        print("Team 2 wins")
    else:
        print("Wow it's still a draw, gotta throw some dices")
    energy_difference = abs(energy_difference)
    print("The energy difference is", energy_difference)
