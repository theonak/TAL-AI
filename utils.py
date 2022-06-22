from random import shuffle
from tensorflow import convert_to_tensor
from champs import champ_to_one_hot, vec_to_champ

def text_to_champ(champs):
    L = champs.split(",")
    return L

def swap(L):
    Lswap = L[1:]
    Lswap.append(L[0])
    return Lswap 

def get_champ(L, encoder, decoder):
    swaps_nb = 300
    proposed_list = []
    proposed_list_amount = []
    for i in range(swaps_nb):
        shuffled_4 = L[:4]
        shuffle(shuffled_4)
        L_test = convert_to_tensor([[champ_to_one_hot(x) for x in shuffled_4]])
        _,_ , vect = encoder(L_test)
        champ = list(decoder(vect).numpy()[0])
        champ_name = vec_to_champ(champ)
        if champ_name in proposed_list:
            proposed_list_amount[proposed_list.index(champ_name)] += 1
        else :
            proposed_list.append(champ_name)
            proposed_list_amount.append(1)
    
    best_champ        = proposed_list[proposed_list_amount.index(max(proposed_list_amount))]
    best_champ_value  = 100*max(proposed_list_amount)/swaps_nb

    return proposed_list, proposed_list_amount, best_champ, best_champ_value

def best_roles(Lsup):
    Ltop = swap(Lsup)
    Ljg = swap(Ltop)
    Lmid = swap(Ljg)
    Ladc = swap(Lmid)
    
    get_champ(Ltop, "top")
    get_champ(Ljg, "jungle")
    get_champ(Lmid, "mid")
    get_champ(Ladc, "adc")
    get_champ(Lsup, "support")
    
  
  
def analysis(l, best_champ, best_champ_value, best_champ_prop, best_champ_pro_value, role, ban1, ban2, other_pick):
    unpickable = ban1 + ban2 + other_pick
    CRED = '\033[91m'
    CBLUE = '\033[94m'
    CGREEN = '\033[92m'
    CEND = '\033[0m'

    if best_champ == l[4]:
        print(CGREEN + "I agree that " + best_champ + " is the best " + role + " in the comp [" + str(best_champ_value) + "%]"  + CEND)
    else:
        if best_champ in unpickable:
            print(CRED + "You were expecting " + l[4] + " as " + role + ". I dont recommend it and " + best_champ + "(Not pickable) is better [" + str(best_champ_value) + "%]" + CEND)
        else:
            if l[4] in best_champ_prop:
                picked_champ_acc = 100*best_champ_pro_value[best_champ_prop.index(l[4])]/300
                print(CBLUE + "You were expecting " + l[4] + " as " + role + ". I recommend him at " + str(picked_champ_acc) + "% but " + best_champ + " is better [" + str(best_champ_value) + "%]"+ CEND)
            else:
                print(CRED + "You were expecting " + l[4] + " as " + role + " but I don't think it's good, " + best_champ + " is better [" + str(best_champ_value) + "%]" + CEND)

def best_roles(Lsup, b1, b2, other_p):
    Ltop = swap(Lsup)
    Ljg = swap(Ltop)
    Lmid = swap(Ljg)
    Ladc = swap(Lmid)
  
    L = [[Ltop, "top"], [Ljg, "jungle"], [Lmid, "mid"], [Ladc, "adc"], [Lsup, "support"]]
    for l in L:
        choices, choices_nb, best, best_acc = get_champ(l[0], l[1]) 
        print(choices)
        print(choices_nb)
        analysis(l[0], best, best_acc, choices, choices_nb, l[1], b1, b2, other_p)

def analyse_game(game):
    game_elems = game.split("	")
    Team1, Team2, Winner, Team1Ban, Team2Ban, Team1Pick, Team2Pick = game_elems
    Team1Ban = text_to_champ(Team1Ban)
    Team2Ban = text_to_champ(Team2Ban)
    Team1Pick = text_to_champ(Team1Pick)
    Team2Pick = text_to_champ(Team2Pick)

    print(Team1)
    best_roles(Team1Pick, Team1Ban, Team2Ban, Team2Pick)
    
    print()
    print(Team2)
    best_roles(Team2Pick, Team1Ban, Team2Ban, Team1Pick)

    print()
    print()

    if Winner == Team1: winningTeam="1"
    else: winningTeam="2"

    print("with this draft, according to you, who wins : '1' or '2' ?")
    guess = input("   ->  ")
    if guess == winningTeam :
        print("En effet, c'est " + Winner + " qui a gagné")
    else:
        print("Non, la draft était pourtant évidente, c'est " + Winner + " qui a gagné")
