'''global variables'''
import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,'Ten':10,'Jack':10,\
          'Queen':10,'King':10,'Ace':11,}

playing = True

'''Card class'''
class Card():
    #Attributes
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
    
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'

'''Deck Class'''
class Deck():
    
    def __init__(self):
        self.deck = []  # start with an empty list 
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank,suit))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+ card.__str__()
        return 'The deck has: '+deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card

'''Hand Class'''
class Hand():
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        
        #track aces
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        #If total value > 21 and I still have an ace, then change my ace to be a 1 instead of 11. 
        while self.value > 21 and self.aces: #and self.aces means if it is greater than 1
            self.value -= 10
            self.aces -= 1
            
    
    def __str__(self):
        hand_comp = ''
        for card in self.cards:
            hand_comp += '\n'+card.__str__()
        return hand_comp

'''Chip Class'''
class Chips():
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -=self.bet


'''Function to take the player's bet'''
def take_bet(playerchips):
    takebet = True
    while takebet == True:
        try:
            playerchips.bet = int(input('\nPlease enter your bet: '))
            if playerchips.bet <= playerchips.total and playerchips.bet > 0:
                print('\n'*100)
                print(f'\nThank you. Your bet is {playerchips.bet}')
                takebet = False
            else:
                print('You cannot bet 0 chips or more than what you have available')
        except:
            print('Error - Please only enter a number.')

'''function to HIT'''
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

'''function to ask player to hit or stand'''
def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:
        try:
            decision = int(input('Would you like to hit or stand? "1" to hit and "2" to stand: '))
            if decision == 1:
                hit(deck,hand)
                print('\n'*100)
                print('\n**HIT**\n')
                show_some(player1_hand,dealer_hand)
                break
            elif decision == 2:
                playing = False
                break
        except:
            print('Only select "1" or "2"')

'''functions to show different hands'''
def show_some(playerhand,dealerhand):
    
    print('******************************************')
    print(f"\nPlayer 1's cards:\n {playerhand}\n")
    print(f"Player 1's value: {playerhand.value}\n")
    print('******************************************')
    print(f"\nDealer's cards: {dealerhand.cards[1]}\n")
    print('******************************************')

def show_all(playerhand,dealerhand):
    print('******************************************')
    print(f"\nPlayer 1's cards:\n {playerhand}\n")
    print(f"Player 1's value: {playerhand.value}\n")
    print('******************************************')
    print(f"\nDealer's cards:\n {dealerhand}\n")
    print(f"Dealer's value: {dealerhand.value}\n")
    print('******************************************')

'''FUNCTIONS TO TEST GAME RESULTS'''
def player_busts(playerhand,playerchips):
    if playerhand.value > 21:
        playerchips.lose_bet()
        print('You Lose. You have busted.')
        return True
    else:
        return False

def player_wins(playerhand,dealerhand,playerchips):
    if playerhand.value > dealerhand.value:
        playerchips.win_bet()
        print("You Win. You have beaten the Dealer's hand.")
        return True
    else:
        return False

def dealer_busts(dealerhand,playerchips):
    if dealerhand.value > 21:
        playerchips.win_bet()
        print('You Win. Dealer has busted.')
        return True
    else:
        return False
    
def dealer_wins(playerhand,dealerhand,playerchips):
    if dealerhand.value > playerhand.value:
        playerchips.lose_bet()
        print("You Lose. The Dealer's hand has beaten yours.")
        return True
    else:
        return False
    
def push(playerhand,dealerhand):
    if playerhand.value == dealerhand.value:
        print('Push')


'''Game Start'''

player1_chips = Chips()
while True:
    # Print an opening statement
    print('Welcome to the Blackjack table.\n')

    
    # Create & shuffle the deck, deal two cards to each player
    playing = True
    gamedeck = Deck()
    gamedeck.shuffle()
    player1_hand = Hand()
    dealer_hand = Hand()
    #dealing
    player1_hand.add_card(gamedeck.deal())
    dealer_hand.add_card(gamedeck.deal())
    player1_hand.add_card(gamedeck.deal())
    dealer_hand.add_card(gamedeck.deal())
    
        
    # Set up the Player's chips
    print(f'\nPlayer 1, you have {player1_chips.total} chips')
    
    # Prompt the Player for their bet
    take_bet(player1_chips)
    print('******************************************\n')
    print('\nShuffling deck...')
    print('Dealing cards...')
    
    
    # Show cards (but keep one dealer card hidden)
    show_some(player1_hand,dealer_hand)
    
    while playing == True:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(gamedeck,player1_hand)
        
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_busts(player1_hand,player1_chips) == True:
            break
        
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
         
        elif playing == False:
            print('\n'*100)
            print('**Stand**\n')
            print('Dealer reveal:\n')
            show_all(player1_hand,dealer_hand)
            while dealer_hand.value < 17:
                print('Dealer HIT')
                hit(gamedeck,dealer_hand)
                show_all(player1_hand,dealer_hand)


                # Show all cards
                # Run different winning scenarios
            else:
                if dealer_busts(dealer_hand,player1_chips) == True:
                    break
                elif player_wins(player1_hand,dealer_hand,player1_chips) == True:
                    break
                elif dealer_wins(player1_hand,dealer_hand,player1_chips) == True:
                    break
                elif push(player1_hand,dealer_hand) == True:
                    break
                                     
    
    # Inform Player of their chips total 
    print(f'\nPlayer 1 has a total of {player1_chips.total} chips\n')
    
    if player1_chips.total <= 0:
        print('You have 0 chips left.')
        break
    
    
    # Ask to play again
    play_again = input('Would you like to play again? (Select Y or N)')
    if play_again.upper() == "Y":
        print('\n'*100)
        pass
    else:
        print('\n'*100)
        break
'''Game End'''
print('\nGame Over. Thanks for playing!')