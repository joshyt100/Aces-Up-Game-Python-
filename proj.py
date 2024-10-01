#########################################################################

#Project 10 
#Game is the "Aces Up" variation of solitaire
#The deck is shuffled and it becomes the stock
#The game also has a tableau and a foundation 
#The tableau is made of four card spots
#The game is won when the stock is empty and only aces are left in
#The tableau
#Program uses different functions and uses the "cards.py" class to
#call different attributes of the stock object
#Input is "D" for deal, "F" for moving a card to the foundation
#"T for moving a card within the tableau, "R" for restart
#"H" for displaying the menu, "Q" for quit

#########################################################################


import cards  
import random

RULES = '''
Aces High Card Game:
     Tableau columns are numbered 1,2,3,4.
     Only the card at the bottom of a Tableau column can be moved.
     A card can be moved to the Foundation only if a higher ranked card 
     of the same suit is at the bottom of another Tableau column.
     To win, all cards except aces must be in the Foundation.'''

MENU = '''     
Input options:
    D: Deal to the Tableau (one card on each column).
    F x: Move card from Tableau column x to the Foundation.
    T x y: Move card from Tableau column x to empty Tableau column y.
    R: Restart the game (after shuffling)
    H: Display the menu of choices
    Q: Quit the game        
'''

def init_game():
    """
    input:no input
    function initalizes game
    returns:object,list of lists,list
    """
    stock = cards.Deck() #deck
    stock.shuffle()#shuffles
    foundation = []
    tableau = []
    tableau.append([stock.deal()])
    tableau.append([stock.deal()])
    tableau.append([stock.deal()])
    tableau.append([stock.deal()])
    
    return stock,tableau,foundation
    
    
def deal_to_tableau( tableau, stock):
    """
    input: list of lists,object
    function deals to the inner lists with the tableau list
    """
    for t in range(len(tableau)):
        if stock.__len__()>0: #checks length of stock
            card=stock.deal()
            tableau[t].append(card) #appends card to each tableau slot


def validate_move_to_foundation( tableau, from_col ):
    """
    input: list of lists,int
    Function determines if requested move to foundation is valid
    Cannot move card form empty column
    returns: boolean
    """
    if not tableau[from_col]: #checking if empty
        print("\nError, empty column:", from_col) #error mesage
        return False
    else:
        t= tableau[from_col][-1]
        suit = t.suit()
        rank = t.rank()
        if rank ==1: #if card is an ace
            print("\nError, cannot move {}.".format(t))
            return False
            
        else:
            j=False
            for i in range(0,len(tableau)):
                if tableau[i]:
                    new_rank = tableau[i][-1].rank() #bottom card rank
                    new_suit = tableau[i][-1].suit() #bottom card suit
                    if new_rank == 1:
                        new_rank = 500 #change ace rank to be higher
                    if suit == new_suit and new_rank>rank: #check against others
                        j=True #variable to see if conditional is true
                        return True
            if not j: #if conditional is not true move cannot be made
                print("\nError, cannot move {}.".format(t))
                return False
        

                    
def move_to_foundation( tableau, foundation, from_col ):
    """
    input: list of lists, list, int
    uses validate_move_to_foundation to determine if 
    card should be moved from tableau to foundation
    """
    if validate_move_to_foundation(tableau,from_col):
        card = tableau[from_col].pop() #removes card and stores in card variable
        foundation.append(card)


def validate_move_within_tableau( tableau, from_col, to_col ):
    """
    input: list of lists, int, int
    function determines if requested move within the tableau is valid
    uses try-excepts to account for empty lists
    returns: boolean
    """
    try:
        moved_card = tableau[from_col][-1] #bottom card
        
    except:
        moved_card = tableau[from_col] #if list is empty
        
    try:
        dest_card= tableau[to_col][-1] #bottom card
    except:
        dest_card= tableau[to_col] #if list is empty

    if dest_card: #checks if list is empty
        print("\nError, target column is not empty: "+str(to_col+1))
        return False
    elif not dest_card and not moved_card: #if both are not empty
        print("\nError, no card in column: "+str(from_col+1))
        return False
    else: # if the one going to is empty
        return True


    
def move_within_tableau( tableau, from_col, to_col ):
    """
    input: list of lists, int, int
    uses validate_move_within_tableau to see 
    if tableau should be changed 
    """
    if validate_move_within_tableau(tableau,from_col,to_col): 
        tableau[to_col].append(tableau[from_col][-1]) #appends bottom card
        tableau[from_col].pop(-1) #removes initial bottom card
          

        
def check_for_win( tableau, stock ):
    """
    input: list of lists, object
    Function checks if the winning conditions have been met
    returns: boolean
    """
    co=0 #counter
    if stock.is_empty(): #checks if stock is empty
        t=True 
        for i in tableau:
            for j in i:
                if j.rank()==1:
                    co+=1 #counts amount of ace cards 
                else: # if there are other cards outside of aces in tableau
                    t=False
                

        if co == 4 and t ==True: #checks to see there are four aces and no others
            return True
        else:
            return False
    else: #if stock isn't empty
        return False
        
            

def display( stock, tableau, foundation ):
    '''Provided: Display the stock, tableau, and foundation.'''

    print("\n{:<8s}{:^13s}{:s}".format( "stock", "tableau", "  foundation"))
    maxm = 0
    for col in tableau:
        if len(col) > maxm:
            maxm = len(col)
    
    assert maxm > 0   # maxm == 0 should not happen in this game?
        
    for i in range(maxm):
        if i == 0:
            if stock.is_empty():
                print("{:<8s}".format(""),end='')
            else:
                print("{:<8s}".format(" XX"),end='')
        else:
            print("{:<8s}".format(""),end='')        
        
        #prior_ten = False  # indicate if prior card was a ten
        for col in tableau:
            if len(col) <= i:
                print("{:4s}".format(''), end='')
            else:
                print( "{:4s}".format( str(col[i]) ), end='' )

        if i == 0:
            if len(foundation) != 0:
                print("    {}".format(foundation[-1]), end='')
                
        print()


def get_option():
    """
    Function prompts for input
    User inputs which option they would like to do 
    Function uses if statements and try-excepts
    to return the respective lists and error messages
    """
    option = input("\nInput an option (DFTRHQ): ") #input
    option_z = option.lower()
    option_m = option_z.split() #make into list
    if option_m[0] == "d":
        if len(option_m)>1: #if there is more than one element in list
            print("\nError in option: " + ' '.join(option.split()))
            return []
        else:
            return ["D"]
    elif option_m[0]== "r":
        return ["R"]
    elif option_m[0] == "h":
        return ["H"]
    elif option_m[0] == "q":
        return ["Q"]
    elif option_m[0]=="f":
        o = option_m
        try:
            try: #tries to make it an int
                o[1]=int(o[1])
            except:
                print("\nError in option: " + ' '.join(option.split()))#error message
                return []

            if 1 <= o[1] <= 4: # checks that it is between 1 and 4
                o[1]-=1
                o[0] = o[0].upper()
                return o
            else:
                raise ValueError
        except ValueError:
            print("\nError in option: " + ' '.join(option.split()))# error message
            return []
    elif option_m[0]=="t":
        o=option.split()
        o[0] = o[0].upper()
        try:
            try:
                o[1]=int(o[1])#tries to int 
                o[2]=int(o[2])#tries to int
            except:
                print("\nError in option: " + ' '.join(option.split()))#error message
                return []

            if 1 <= o[1] <= 4 and 1 <= o[2] <= 4: #both values are between 1 and 4
                o[1]-=1 #decrease by 1 for indexing purposes
                o[2]-=1 #decrease by 1 for indexing purposes
                return o
            else:
                raise ValueError
        except ValueError:
            print("\nError in option: " + ' '.join(option.split()))
            return []
    else:#if user puts anything than else than provided
        
        print("\nError in option: " + ' '.join(option.split()))
        return []

    

        
        
        
def main():
    
    print(RULES)
    print(MENU)
    attempt = True
    stock,tableau,foundation = init_game() #initialize game
    display(stock,tableau,foundation) #displays starting game
    option = get_option() #prompt for option

    while attempt:
        if option:
            if option==['D']: #Deals cards
                deal_to_tableau( tableau, stock) #deals

            elif option[0]=="F": #Moves card to foundation
                
                move_to_foundation( tableau, foundation, option[1] ) #moves to foundation
                    
                
            elif option[0] == "T": #moves card within the tableau
                move_within_tableau( tableau, option[1], option[2] ) 
                
            elif option == ['H']:#prints menu
                print(MENU) 
            elif option == ['R']: # restarts game 
                print("\n=========== Restarting: new game ============") 
                print(RULES)
                print(MENU)
                stock,tableau,foundation = init_game() #reinitialize variables
                
        
    
            elif option == ['Q']: #quits game 
                print("\nYou have chosen to quit.") #message
                attempt = False
                break
            
            if not check_for_win(tableau,stock): #checks that game hasn't been won
                display(stock,tableau,foundation)
            else:
                print("\nYou won!") #winning message
                break #breaks if game is won
        option = get_option() #prompts for next option
        
        


if __name__ == '__main__':
     main()

