# A Hammurabi game (ver 0.0.1)
# written by Zhishen (Jason) Wen, MCIT, Penn CIS, Sept. 2012

import random, string

def hammurabi():
    # hammurabi main function

    # initialize variables
    starved = 0
    immigrants = 5
    population = 100
    harvest = 3000 # bushels
    bushels_per_acre = 3 # amount harvested
    rats_ate = 200 # bushels
    bushels_in_storage = 2800
    acres_owned = 1000
    cost_per_acre = 19 # bushels per acre
    plague_deaths = 0
    print_introductory_message()

    # begin a ten year loop and print the outcome of each year
    for year in range(1, 11):
        print "O great Hammurabi!"
        print "You are in year", year, "of your ten year rule."
        print "In the previous year", starved, "people starved to death."
        print "In the previous year", immigrants, "people entered the kingdom."
        print "The population is now", str(population) + "."
        print "We harvested", harvest, "bushels at", bushels_per_acre, "bushels per" \
        " acre."
        print "Rats destroyed", rats_ate, "bushels, leaving", bushels_in_storage, "" \
        "bushels in storage."
        print "The city owns", acres_owned, "acres of land."
        print "Land is currently worth", cost_per_acre, "bushels per acre."
        print "There were", plague_deaths, "deaths from the plague."
        print

        # ask a series of questions
        acres_bought = ask_to_buy_land(bushels_in_storage, cost_per_acre)
        if acres_bought:
            acres_owned += acres_bought
            bushels_in_storage -= acres_bought * cost_per_acre
        else:
            # do not ask user to sell land if s/he is buying land
            acres_sold = ask_to_sell_land(acres_owned, cost_per_acre)
            acres_owned -= acres_sold
            bushels_in_storage += acres_sold * cost_per_acre
        bushels_fed = ask_to_feed_people(bushels_in_storage, population)
        bushels_in_storage -= bushels_fed
        acres_planted = ask_to_plant_land(population, bushels_in_storage)
        bushels_in_storage -= acres_planted * 2

        # determine the consequences
        plague_deaths = do_plague(population)
        population -= plague_deaths
        starved = get_starved_num(population, bushels_fed)
        do_dismissal_for_starv(starved, population, year)
        population -= starved
        immigrants = get_immigrts_num(acres_owned, bushels_in_storage,
                                      population, starved)
        population += immigrants
        bushels_per_acre = get_unit_havst()
        harvest = get_havst_bushels(acres_planted, bushels_per_acre)
        rats_ate = do_rat_infestation(harvest)
        bushels_in_storage += harvest - rats_ate
        cost_per_acre = get_land_price()
        print

    # print out a final summary
    summarize_result(acres_owned, bushels_in_storage, population, starved)
    # the end of hammurabi main function
        
# definitions of other functions
def print_introductory_message():
    print """Congratulations, you are the newest ruler of ancient Samaria, elected
for a ten year term of office. Your duties are to dispense food, direct
farming, and buy and sell land as needed to support your people. Watch
out for rat infestations and the plague! Grain is the general currency,
measured in bushels. The following will help you in your decisions:

  * Each person needs at least 20 bushels of grain per year to survive.

  * Each person can farm at most 10 acres of land.

  * It takes 2 bushels of grain to farm an acre of land.

  * The market price for land fluctuates yearly.

Rule wisely and you will be showered with appreciation at the end of
your term. Rule poorly and you will be kicked out of office!"""

def ask_to_buy_land(bushels, cost):
    # ask user how many acres of land to buy
    acres = get_int("How many acres of land will you buy? (0 to DECLINE)\n")
    while acres * cost > bushels:
        print "O great Hammurabi, we have but", bushels, "bushels of grain!"
        print acres, "acres are too many to afford to buy!"
        acres = get_int("Again, how much land will you buy? (0 to DECLINE)\n"
                        "[HINT: The maximum of current purchasing power is " + str(
                        bushels / cost) + " acres.]\n")
    return acres

def ask_to_sell_land(curr_acres, cost):
    # ask user how many acres of land to sell
    acres = get_int("How many acres of land will you sell?\n")
    while acres > curr_acres:
        print "O great Hammurabi, we have but", curr_acres, "acres of land!"
        print acres, "acres exceed our land limit!"
        acres = get_int("Again, how much land will you sell?\n[HINT: Current land "
                        "price is " + str(cost) + ".]\n")
    return acres

def ask_to_feed_people(curr_bushels, num_of_people):
    # ask user how many bushels of grain to feed to the people
    bushels = get_int("How many bushels of grain will you feed to the people?\n")
    while bushels > curr_bushels:
        print "O great Hammurabi, we have but", curr_bushels, "bushels" \
        " of grain!", bushels, "bushels exceed our grain reserves!"
        bushels = get_int("Again, how much grain will you feed to the people?\n[H"
                          "INT: In order for everyone to survive, current populat"
                          "ion needs at least total amount of " +
                          str(num_of_people * 20) +" bushels.]\n")
    return bushels

def ask_to_plant_land(num_of_people, bushels):
    # ask user how many acres of land to plant with seed
    acres = get_int("How many acres of land will you plant with seed?\n")
    while True:
        if acres > num_of_people * 10:
            print "O great Hammurabi, we have but", num_of_people, "people that can " \
            "farm the land!"
            print acres, "acres are too many for us! We still need more people to do" \
            " the job!"
            acres = get_int("Please factor our manpower. Again, how much land will y"
                            "ou plant?\n[HINT: The maximum possible acres of current"
                            " total labor force that can afford to farm is " +
                            str(num_of_people * 10) + " acres.]\n")
            continue
        if bushels < acres * 2:
            print "O great Hammurabi, we have but", bushels, "bushels to spend farmi" \
            "ng the land!"
            print acres, "acres are too many for us! We lack enough bushels to start" \
            " our farming!"
            acres = get_int("Please factor our funds. Again, how much land will you "
                            "plant with seed?\n[HINT: The maximum possible acres of "
                            "current total funds to spend farming is " +
                            str(bushels / 2) + " acres.]\n")
            continue
        break
    return acres

def do_plague(num_of_people):
    # simulate whether or not a plague happened and return a consequence
    if random.randint(0, 99) < 15:
        print "***O great Hammurabi, unluckily a horrible PLAGUE" \
        " happened!", num_of_people / 2, "people died***"
        return num_of_people / 2
    else:
        print "***Thank God! No plague this year***"
        return 0

def get_starved_num(num_of_people, grain_fed):
    # get the number of people starved this year
    num_of_the_starved = num_of_people - grain_fed / 20
    if num_of_the_starved > 0:
        print "***O great Hammurabi, unfortunately this year we " \
        "have", num_of_the_starved, "PEOPLE STARVED***"
        return num_of_the_starved
    else:
        print "***O brilliant Hammurabi! This year we have NO people starved***"
        return 0

def do_dismissal_for_starv(num_of_the_starved, num_of_people, yr):
    # judge whether or not the user should be dismissed according
    # to the numbers of people starved
    if num_of_the_starved > 0.45 * num_of_people:
        print "***O great Hammurabi, we  really regret to inform you that this " \
        "year", num_of_the_starved, "people have been starved, which represent " \
        "more than 45% of total population in your Samaria kingdom. According t" \
        "o our laws, you're now unfortunately given an immediate dismissal requ" \
        "est***"
        game_ends(yr)

def get_immigrts_num(acres, bushels, num_of_people, num_of_the_starved):
    # get the number of immigrants to our country this year
    if num_of_the_starved:
        print "***O great Hammurabi, due to starvation, NO IMMIGRANTS this year" \
        " come to our kingdom***"
        return 0
    else:
        num_of_immigrts = (20 * acres + bushels) / (100 * num_of_people) + 1
        print "***O great Hammurabi, this year", num_of_immigrts, "immigrants c" \
        "ome to our kingdom***"
        return num_of_immigrts

def get_havst_bushels(acres, unit_havst):
    # get bushels of grain harvested this year
    bushels_havst =  acres * unit_havst
    print "***O great Hammurabi, this year we harvest", bushels_havst, "bushels" \
    " of grain***"
    return bushels_havst

def get_unit_havst():
    # get bushels per acre yielded
    return random.randint(1, 8)

def do_rat_infestation(havst):
    # simulate whether or not a rat infestation happened and return a consequence
    if random.randint(0, 99) < 40: 
        bushels_destroyed = random.randint(10, 30) * havst / 100
        print "***O great Hammurabi, unluckily a horrible RAT INFESTATION happe" \
        "ned!", bushels_destroyed, "bushels of grain were destroyed***"
        return bushels_destroyed
    else:
        print "***Thank God! No rat infestation occurred this year***"
        return 0

def get_land_price():
    # get the price of land next year
    land_price = random.randint(17, 23)
    print "***O great Hammurabi, the price of land will be", land_price, "bushe" \
    "ls per acre next year***"
    return land_price

def summarize_result(acres, bushels, num_of_people, num_of_the_starved):
    # print a summary regarding your play evaluated by acres of land,
    # bushels of grain, total population, and number of the starved
    print "===================== C O N G R A T U L A T I O N S !======================"
    print "    Hammurabi your highness, you've successfully gone through your ten"
    print "    year term of office."
    print "    In the end of your term of reign, the Samaria Kingdom:"
    print
    print "  * owns", acres, "acres of wealthy land;"
    print "  * owns", bushels, "bushels of grain in storage;"
    print "  * has a total population of", str(num_of_people) + ";"
    print "  * has", num_of_the_starved, "people starved."
    print
    print eval_acres(acres)
    print eval_bushels(bushels)
    print eval_population(num_of_people)
    print eval_starved(num_of_the_starved)
    print "=================== G A M E ===== A C C O M P L I S H E D ================="
    print
    print "                  *** THANK YOU FOR PLAYING HAMMURABI! ***"

def eval_acres(acres):
    # evaluate acres of land you own
    if acres > 1550:
        strg = "O great Hammurabi, you've done very well in keeping the realm of our k" \
        "ingdom increasing. Fantastic!"
    elif acres > 1000:
        strg = "O great Hammurabi, you've well maintained our land size as it was ten " \
        "years ago, though our domain expanded little!"
    elif acres > 500:
        strg = "O great Hammurabi, you've lost some of our land! That's a pity. You co" \
        "uld have done better!"
    else:
        strg = "O great Hammurabi, our fruitful land has been shrinked dramatically un" \
        "der your rule. That's really not good!"
    return strg

def eval_bushels(bushels):
    # evaluate bushels of grain you own
    if bushels > 18000:
        strg = "Nice job! You have earned a lot to feed and finance our homeland. That" \
        "'s really cool!"
    elif bushels > 10000:
        strg = "Steady increase of bushels. Our country is wealthy!"
    elif bushels > 2800:
        strg = "Fine policies, but haven't earned much. We need more bushels to thrive!"
    else:
        strg = "Oops, you haven't handled your financial task well. So much grain lost!"
    return strg

def eval_population(num_of_people):
    # evaluate total number of people you have
    if num_of_people > 200:
        strg = "There are more than twice people now living in Samaria as ten years ago."
    elif num_of_people > 130:
        strg = "During your term of office, population here increases pretty steadily."
    elif num_of_people > 95:
        strg = "During the ten years, total number of people in Samaria changed little."
    else:
        strg = "In the end of your reign, total population decreased."
    return strg

def eval_starved(num_of_the_starved):
    # evaluate number of people starved
    if num_of_the_starved > 70:
        strg = "In the end of your term more than 70 citizens starved to death. That's" \
        " an extremely serious problem!"
    elif num_of_the_starved > 30:
        strg = "In the end of your term at least 30 people died from starvation. Every" \
        " citizen's basic living requirements should be met!"
    elif num_of_the_starved > 0:
        strg = "In the end of your term, still some people starved to die. This could " \
        "have been avoided by a reasonable farming policy."
    else:
        strg = "That's great because now no one starved in our country!"
    return strg

def game_ends(yr):
    print "========================== G A M E ===== O V E R =========================="
    print "       O great Hammurabi, we're truly regretful that in year", yr, "of"
    print "       your ten year rule, you lost your imperial authority."
    print
    print "                 *** THANK YOU FOR PLAYING HAMMURABI! ***"
    quit()
    
def get_int(message):
    # print the message as prompt, and ask the user to enter an unsigned integer
    answer = None
    while answer == None:
        try:
            answer = int(input(message))
        except:
            print "[Please re-enter a valid number. Signed int will be transformed t" \
            "o unsigned automatically.]"
    return abs(answer)
