def AI_dumb(werewolf_dico, food_dico, team):

    """
    AI to test the code.

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
    specification : Alexis Regardin (v.2 15/03/2022)
    implementation : Alexis Regardin (v.4 27/03/2022)
    """

    orders = ''
    AI_wolves = []
    enemy_wolves = []

    for location in werewolf_dico: #Create a list of all the wolves of the AI's team
        if werewolf_dico[location][0] == team:
            if werewolf_dico[location][1] == 'omega':
                pacify_rate = randint(1,3) #The omega has a 1 in 3 chance of pacifying
                if pacify_rate == 3:
                    location = (location.strip('[',))
                    location = location.strip(']')
                    location = location.split(',')
                    x_position_origin = int(location[0])
                    y_position_origin = int(location[1])
                    origin_position = str(x_position_origin) + '-' + str(y_position_origin) #Create something we can use for the order : x-y 
                    pacify_order = (origin_position + ':Pacify')
                    orders += (pacify_order + ' ')
            else:
                AI_wolves.append(location) 

    for location in werewolf_dico: #Create a list of all the wolves of the enemy
        if werewolf_dico[location][0] != team:
            enemy_wolves.append(location)

    for wolves in AI_wolves:
        wolves_coordinate = (wolves.strip('[',))
        wolves_coordinate = wolves_coordinate.strip(']')
        wolves_coordinate = wolves_coordinate.split(',')
        #Gives us 2 elements in a list: [x, y]
        x_position_origin = int(wolves_coordinate[0])
        y_position_origin = int(wolves_coordinate[1]) #Keep the x and y coordinate of the wolf from the AI's team
        
        for enemy in enemy_wolves:
            if werewolf_dico[enemy][2] > 0:
                enemy = (enemy.strip('[',))
                enemy = enemy.strip(']')
                enemy = enemy.split(',') #Gives us 2 elements in a list: [x,y]
                x_position_target = int(enemy[0])
                y_position_target = int(enemy[1])

            x_difference = x_position_target - x_position_origin
            y_difference = y_position_target - y_position_origin
            total_difference = x_difference * y_difference
            if total_difference in [-1,0,1] and x_difference in [-1,0,1] and y_difference in [-1,0,1]: #Check if the target is 0 or 1 square away from the origin 
                    origin_position = str(x_position_origin) + '-' + str(y_position_origin)
                    target_position = str(x_position_target) + '-' + str(y_position_target) 
                    order_turn = (origin_position + ':*' + target_position) #Create an attack order like this : x-y:*x-y 

                    orders += (order_turn + ' ') #Add the order 

        for wolves in AI_wolves:
            if werewolf_dico[wolves][2] < 100: #The wolf has less than 100 energy
                for food in food_dico:
                    food = (food[0].strip('[',))
                    food = food.strip(']')
                    food = food.split(',')
                    #Gives us 2 elements in a list: [x,y]
                    x_position_target = int(food[0])
                    y_position_target = int(food[1])
                    x_difference = x_position_target - x_position_origin
                    y_difference = y_position_target - y_position_origin
                    total_difference = x_difference * y_difference
                    if total_difference in [-1,0,1] and x_difference in [-1,0,1] and y_difference in [-1,0,1]: #Check if the target is 0 or 1 square away from the origin 
                        origin_position = str(x_position_origin) + '-' + str(y_position_origin)
                        target_position = str(x_position_target) + '-' + str(y_position_target) 
                        order_turn = (origin_position + ':<' + target_position) #Create a eat order like this : x-y:<x-y 
                        orders += (order_turn + ' ')
            else: #The wolf has already 100
                x_position_moving = x_position_origin + randint(-1,1)
                y_position_moving = x_position_origin + randint(-1,1)
                order_turn = (str(x_position_origin) + '-' + str(y_position_origin) + ':@' + str(x_position_moving) + '-' + str(y_position_moving))
                orders += (order_turn + ' ')

    orders = str(orders)
    return orders


#def distance_finder(enemy_dico)


