from hanabi.ai import AI
from hanabi.deck import Color
from random import randint

#On essaye d'implémenter la technique du chapeau à 5 joueurs

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
#choix de l'action a effectué en fonction de la main du joueur (playable card, most recent recomandation, no card played, hint tokken, discardable card)
#			=>playable card : laquelle ?
#			=>hint : à qui et quoi ?
#			=>dicardable card : indice le plus faible
#maj du tableau de jeu 


	def action():
#priorité action 1 : si la dernière recommandation était de jouer une carte et que personne n'a joué de carte entre temps alors joué la carte
		if
#action 2 : si la dernière recommandation était de jouer une carte et que une personne a joué une carte entre temps mais qu'il reste moins de deux erreurs alors joué la carte
		if
#action 3 : si on peut donner un indice on le donne
		if
#action 4 : si la dernière recommandation était de jeter une carte, jetée la carte
		else 
#action 5 : carte c1 jetée







	def play_card_priority():
		game=self.game
#priorité indice 1 : carte chiffre 5 jouable doit etre jouée avec le ci le plus petit
		if
#Indice 2 : carte avec le plus petit chiffre jouable soit jouée, si plusieurs alors ci le plus petit
		if
#Indice 3 : carte inutile avec le plus petit ci soit jetée
		if
#Indice 4 : carte avec le chiffre le plus haut et non indispensable soit jetée, si plusieurs ci le plus petit
		else 
#Indice 5 : carte c1 jetée
