#pseudo-code
 
#0.Play card c1  4.Discard card c1
#1.Play card c2  5.Discard card c2
#2.Play card c3  6.Discard card c3
#3.Play card c4  7.Discard card c4

"""
Artificial Intelligence to play Hanabi.
"""

import itertools
import random

class Robot(AI):

	def __init__(self, game):
        self.game = game


	def play(self):
		 game = self.game
		 jouables = [ i+1 for i in
                     enumerate(game.current_hand.cards)
                     if card.recommanded = True]#Remplacer par une boucle qui checke le flag recommanded et risky
		 mortes = [ i+1 for i in
                     enumerate(game.current_hand.cards)
                     if card.dead = True]#Remplacer par une boucle qui checke le flag dead
#choix de l'action a effectuer en fonction de la main du joueur (playable card, most recent recomandation, no card played, hint tokken, discardable card)
#			=>playable card : laquelle ?
#			=>hint : à qui et quoi ?
#			=>dicardable card : indice le plus faible
#maj du tableau de jeu 
		if (jouables!=[] and jouable[0].risky == False):
			return("p%d",jouables[0])
		elif (jouables!=[] and jouable[0].risky == True and )
#action 3 : si on peut donner un indice on le donne
		if (blue_coins>0):
			
#action 4 : si la dernière recommandation était de jeter une carte, jetée la carte
		if mortes != []:
			return("d%d",mortes[0])
#action 5 : carte c1 jetée
		else
			return("d1")


	
	#def number (self) : #calcul le nombre pour savoir l'indice 
		


# 	def play_card_priority():
# 		game=self.game
# #priorité indice 1 : carte chiffre 5 jouable doit etre jouée avec le ci le plus petit
# 		if
# #Indice 2 : carte avec le plus petit chiffre jouable soit jouée, si plusieurs alors ci le plus petit
# 		if
# #Indice 3 : carte inutile avec le plus petit ci soit jetée
# 		if
# #Indice 4 : carte avec le chiffre le plus haut et non indispensable soit jetée, si plusieurs ci le plus petit
# 		if 
# #Indice 5 : carte c1 jetée
# 		else 
# 			return ("d1")
"""
	def what_clue (self,c_or_r) : #retourne quel indice donnée au joueur choisi en fonction de si on doit lui donner color or rank
		if (c_or_r==c):
			
		if (c_or_r==r):
"""