#Functions for the AI

def differences(location, x_origin, y_origin):
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
    location[1] = location[1].strip(' ')

    return location

def AI_attack(x_position_origin, y_position_origin, x_position_target, y_position_target):
    """
    Attacks of the AI

    Parameters :
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
    implementation : Alexis Regardin (v.5 01/05/2022)
    """

    orders = ''
    order_turn = ''

    AI_wolves = []
    enemy_wolves = []
            
    for AI_location in werewolf_dico:
        if werewolf_dico[AI_location][0] == team:
            if werewolf_dico[AI_location][1] == 'omega' and werewolf_dico[AI_location][2] > 40: #The omega wont become an human
                omega_location = splitter(AI_location)
                x_position_origin = int(omega_location[0])
                y_position_origin = int(omega_location[1])
                for enemy in werewolf_dico:
                    if werewolf_dico[enemy][0] != team:
                        location = splitter(enemy)
                        result = differences(location, x_position_origin,y_position_origin) 
                        if result[0] in range(-6,6) and result[1] in range(-6,6): #There is an enemy in the area
                            origin_position = str(x_position_origin) + '-' + str(y_position_origin) #Create something we can use for the order : x-y 
                            pacify_order = (origin_position + ':Pacify')
                            orders += (pacify_order + ' ')

    for wolves in werewolf_dico:
        if werewolf_dico[wolves][0] == team:
            AI_wolves.append(wolves)
    
    for enemy in werewolf_dico:
        if werewolf_dico[enemy][0] != team:
            enemy_wolves.append(enemy)
            
    for wolves in AI_wolves:
        wolves_coordinate = splitter(wolves)
        x_position_origin = int(wolves_coordinate[0])
        y_position_origin = int(wolves_coordinate[1]) #Keep the x and y coordinate of the wolf from the AI's team    for enemy in werewolf_dico:
        
        
        if werewolf_dico[wolves][2] > 10: #If the wolf has enough energy left to fight 
            for enemy in enemy_wolves:
                enemy_coordinate = splitter(enemy)
                x_position_target = int(enemy_coordinate[0])
                y_position_target = int(enemy_coordinate[1])
                x_difference = x_position_target - x_position_origin
                y_difference = y_position_target - y_position_origin
                total_difference = x_difference * y_difference
                #Will attack any wolf next to him
                if total_difference in [-1,0,1] and (x_position_target - x_position_origin) in [-1,0,1] and (y_position_target - y_position_origin) in [-1,0,1]: #Check if the target is 0 or 1 square away from the origin 
                        if werewolf_dico[enemy][2] > 0: #The enemy has more than 0 life left                 
                            order_turn = AI_attack(x_position_origin, y_position_origin, x_position_target, y_position_target) #Create an attack order like this : x-y:*x-y 
                            orders += (order_turn + ' ')
                else: #The wolf isn't next to any wolves
                    for alpha in enemy_wolves:
                        if werewolf_dico[alpha][0] == 'alpha':
                            enemy_coordinate = splitter(alpha)
                            x_position_target = int(enemy_coordinate[0])
                            y_position_target = int(enemy_coordinate[1])
                            x_difference = x_position_target - x_position_origin
                            y_difference = y_position_target - y_position_origin
                            total_difference = x_difference * y_difference
                    if x_difference < -1:
                        x_position_target = x_position_origin - 1 
                    elif x_difference > 1:
                        x_position_target = x_position_origin + 1     
                    else:
                        x_position_target = x_position_origin
                    if y_difference < -1:
                        y_position_target = y_position_origin - 1
                    elif y_difference > 1:
                        y_position_target = y_position_origin + 1
                    else:
                        y_position_target = y_position_origin
                    origin = str(x_position_origin) + '-' + str(y_position_origin)
                    target = str(x_position_target) + '-' + str(y_position_target)
                    order_turn = origin + ':@' + target
                    orders += (order_turn + ' ')
        elif werewolf_dico[wolves][2] <= 10: #The wolf has few energy left, there is still food left, send him to the nearest food
            for food in food_dico:
                food = splitter(food)
                x_position_target = int(food[0])
                y_position_target = int(food[1])
                x_difference = x_position_target - x_position_origin
                y_difference = y_position_target - y_position_origin
                total_difference = x_difference * y_difference
                
                if total_difference in range(-1,1) and (x_position_target - x_position_origin) in range(-1,1) and (y_position_target - y_position_origin)  in range(-1,1): #Check if the target is 0 or 1 square away from the origin
                    origin_position = str(x_position_origin) + '-' + str(y_position_origin)
                    target_position = str(x_position_target) + '-' + str(y_position_target) 
                    order_turn = (origin_position + ':<' + target_position) #Create a eat order like this : x-y:<x-y 
                    orders += (order_turn + ' ')
                else:
                    if total_difference in range(-5,5) :
                        if x_difference < -1:
                            x_position_target = x_position_origin - 1                                   
                        elif x_difference > 1:
                            x_position_target = x_position_origin + 1
                        else:
                            x_position_target = x_position_origin
                        if y_difference < -1:
                            y_position_target = y_position_origin - 1
                        elif y_difference > 1:
                            y_position_target = y_position_origin + 1
                        else:
                            y_position_target = y_position_origin
                        origin = str(x_position_origin) + '-' + str(y_position_origin)
                        target = str(x_position_target) + '-' + str(y_position_target)
                        order_turn = origin + ':@' + target
                        orders += (order_turn + ' ')
                    elif total_difference in range(-10,10):
                        if x_difference < -1:
                            x_position_target = x_position_origin - 1                                   
                        elif x_difference > 1:
                            x_position_target = x_position_origin + 1
                        else:
                            x_position_target = x_position_origin
                        if y_difference < -1:
                            y_position_target = y_position_origin - 1
                        elif y_difference > 1:
                            y_position_target = y_position_origin + 1
                        else:
                            y_position_target = y_position_origin
                        origin = str(x_position_origin) + '-' + str(y_position_origin)
                        target = str(x_position_target) + '-' + str(y_position_target)
                        order_turn = origin + ':@' + target
                        orders += (order_turn + ' ')
                    
    orders = str(orders)
    return orders
