"""
File name: memory.py
Author: Bret Silverstein
Date created: 10/5/2019
Python Version: 3.6

This is a game called memory (or concentration). The objective is to match cards with the
same color and rank until every card in the deck is matched.
"""

import pandas as pd
import numpy as np
import sys
import random
import time
import re

#Play game in a loop
def main():
    pd.set_option('expand_frame_repr', False)

    instructions()
    size = [4, 13]
    deck = buildDeck() 
    bestScore = float('inf')
    again = 'y'
    
    while (again == 'y'):
        again, score = play(size, deck) 
        if (score < bestScore):
            bestScore = score
        print('Best Score: '+str(bestScore))

#Print instructions
def instructions():  
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('* Welcome to Memory!')
    print('* To select a card enter the row and column number seperated by a space.')
    print('* A pair is made if you select two cards with the same rank and color.')
    print('* Incorrect guesses will only be visible for 5 seconds. Watch closely!') 
    print('* The game will end when you match each pair correctly.')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    
#Create a deck; list of Card objects
def buildDeck():
    deck = []
    for suit in ['H','D','S','C']:
        for value in range(2,11):
            deck.append(Card(str(value),suit))
        for value in ['J','Q','K','A']:
            deck.append(Card(value,suit))
    return deck

#Play the game given the size of the board and the deck to use
def play(size, deck):
    cardsToUse = random.sample(deck, size[0]*size[1])
    cardsArray = [cardsToUse[i:i+size[1]] for i in range(0,len(cardsToUse),size[1])]
    solution   = pd.DataFrame(np.array(cardsArray))
    boardShown = pd.DataFrame('[~]', index=range(size[0]), columns=range(size[1]))
    
    pairs = 0
    guesses = 0
    pairList = []
    while (pairs != 26):
        printBoard(boardShown, pairs, guesses)
        
        chosen = chooseCards(size)
        r1 = int(chosen[0][0])
        c1 = int(chosen[0][1])
        r2 = int(chosen[1][0])
        c2 = int(chosen[1][1])

        tempBoard = boardShown.copy()
        tempBoard.iloc[r1,c1] = solution.iloc[r1,c1]
        tempBoard.iloc[r2,c2] = solution.iloc[r2,c2]
        
        guesses += 1
        if ((tempBoard.iloc[r1,c1] == tempBoard.iloc[r2,c2]) 
                and ([r1,c1] not in pairList) and ([r2,c2] not in pairList)):
            pairs += 1
            boardShown = tempBoard
            pairList = pairList + [[r1,c1]] + [[r2,c2]]
        
        #Wrong guess
        else:
            for i in reversed(range(5)):
                for j in range(100):
                    print(' ') 
                print('TIME: '+str(i))
                printBoard(tempBoard, pairs, guesses)
                time.sleep(1)
            for i in range(100):
                print(' ')

    print('Congrats, you win!')
    print('Score: '+str(guesses))
    return (input('Play again? Type \'y\': '), guesses)

#Choose two cards and check for bad input
def chooseCards(size):
    badInput = 1
    while badInput:
        chosen1 = input('Choose the first card: ')
        chosen1 = re.split(' ',chosen1)
        
        #Check input for first card chosen
        if (len(chosen1) != 2 or not chosen1[0].isdigit() or not chosen1[1].isdigit()
                or int(chosen1[0]) >= size[0] or int(chosen1[1]) >= size[1]):
            print('Enter the row and column numbers seperated by a space.')
        else:
            chosen2 = input('Choose the second card: ')
            chosen2 = re.split(' ',chosen2)

            #Check input for second card chosen
            if (len(chosen2) != 2 or not chosen2[0].isdigit() or not chosen2[1].isdigit()
                    or int(chosen2[0]) >= size[0] or int(chosen2[1]) >= size[1]
                    or chosen2 == chosen1):
                print('Enter the row and column numbers seperated by a space.')
            else:
                badInput = 0

    return [chosen1,chosen2]

def printBoard(board, pairs, guesses): 
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('Pairs Made: ' + str(pairs))
    print('Guesses Made: ' + str(guesses))
    print(board)
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

#Card class which keeps track of rank, suit, and color of each card
class Card:
    #Domain of rank: 2-10,J,Q,K,A
    #Domain of suit: H,D,S,C
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        
        if ((self.suit == 'H') or (self.suit == 'D')):
            self.color = 'red'
        else:
            self.color = 'black'

    def __str__(self):
        return self.rank+'('+self.suit+')'
    
    def __eq__(self, other):
        if ((self.rank == other.rank) and (self.color == other.color)):
            return True
        return False
    
if __name__ == "__main__":
    main()
