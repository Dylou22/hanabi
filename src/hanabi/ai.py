"""
Artificial Intelligence to play Hanabi.
"""

import itertools


class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game):
        self.game = game

    @property
    def other_hands(self):
        "The list of other players' hands."
        return self.game.hands[1:]

    @property
    def other_players_cards(self):
        "All of other players's cards, concatenated in a single list."
        # return sum([x.cards for x in self.other_hands], [])
        return list(itertools.chain.from_iterable([hand.cards for hand in self.other_hands]))

class Robot(AI):
    def play(self):
        """Renvoie la meilleure action en suivant l'algorithme du chapeau :
        1. Jouer une carte recommandée et non risquée
        2. Jouer une carte recommandée et risquée si il y a moins de 2 jetons rouges
        3. Donner un indice
        4. Défausser une carte morte
        5. Défausser c1. /!\ Nous avons implémenté une variante : si le joueur sait (grâce à l'indice réel) que c1 est un 5, il défausse alors c2. Si il sait que c1 et c2 sont des 5 alors c3, etc"""
        game = self.game
        jouables = [ i+1 for (i,card) in enumerate(game.current_hand.cards) if card.recommanded == True]
        mortes = [ i+1 for (i,card) in enumerate(game.current_hand.cards) if card.dead == True]
        # 1. Jouer une carte recommandée et non risquée
        if (jouables!=[]):
            for (i,card) in enumerate (game.current_hand.cards) :
                if (card.risky == False and card.recommanded==True):
                    return("p%d"%(i+1))
                # 2. Jouer une carte recommandée et risquée si il y a moins de 2 jetons rouges
                elif(card.risky == True and card.recommanded==True and game.red_coins < 2):
                    return("p%d"%(i+1))

        #3. Donner un indice
        if (game.blue_coins>0):#3.Donner un indice
            n_propre = game.somme_joueurs
            if n_propre == 0:
                return("c51")
            if n_propre == 1:
                return("c52")
            if n_propre == 2:
                return("c53")
            if n_propre == 3:
                return("c54")
            if n_propre == 4:
                return("cR1")
            if n_propre == 5:
                return("cR2")
            if n_propre == 6:
                return("cR3")
            if n_propre == 7:
                return("cR4")
        #Défausser une carte morte
        if mortes != []:
            #print ("mortes=",mortes)
            return("d%d"%mortes[0])
        
        #5. Défausser c1. /!\ Nous avons implémenté une variante : si le joueur sait (grâce à l'indice réel) que c1 est un 5, il défausse alors c2. Si il sait que c1 et c2 sont des 5 alors c3, etc
        else:
            if game.current_hand.cards[0].number_clue == "5" :#NB : number_clue est soit False (à l'initialisation), soit un caractère entre 1 et 5
                if game.current_hand.cards[1].number_clue == "5" :
                    if game.current_hand.cards[2].number_clue == "5" :
                        return ("d4")
                    return ("d3")
                return ("d2")
            return("d1")


class Cheater(AI):
    """
    This player can see his own cards!
    Algorithm:
      * if 1-or-more card is playable: play the lowest one, then newest one
      * if blue_coin<8 and an unnecessary card present: discard it.
      * if blue_coin>0: give a clue on precious card (so a human can play with a Cheater)
      * if blue_coin<8: discard the largest one, except if it's the last of its kind or in chop position in his opponent.
    """
    def play(self):
        "Return the best cheater action."
        game = self.game
        playable = [ (i+1, card.number) for (i, card) in
                     enumerate(game.current_hand.cards)
                     if game.piles[card.color]+1 == card.number ]
        if playable:
            # sort by ascending number, then newest
            playable.sort(key=lambda p: (p[1], -p[0]))
            return "p%d"%playable[0][0]
        discardable = [ i+1 for (i, card) in enumerate(game.current_hand.cards) if ( (card.number <= game.piles[card.color]) or (game.current_hand.cards.count(card) > 1)) ]
        if discardable and (game.blue_coins < 8):
            return "d%d"%discardable[0]
        discardable2 = [ i+1 for (i, card) in enumerate(game.current_hand.cards)
                         if card in self.other_players_cards
                       ]
        if discardable2 and (game.blue_coins < 8):
            return "d%d"%discardable2[0]
        precious = [ card for card in self.other_players_cards if (1+game.discard_pile.cards.count(card)) == game.deck.card_count[card.number]]
        if precious:
            clue = False
            for p in precious:
                if p.number_clue is False:
                    clue = "c%d"%p.number
                    break
                if p.color_clue is False:
                    clue = "c%s"%p.color
                    clue = clue[:2]
                    break
            if clue:
                if game.blue_coins > 0:
                    return clue
        if game.blue_coins > 0:
            return 'cw'
        mynotprecious = [ (card.number, i+1) for (i, card) in
                          enumerate(game.current_hand.cards)
                          if not (
                                  (1+game.discard_pile.cards.count(card))
                                  == game.deck.card_count[card.number])
                     ]
        mynotprecious.sort(key=lambda p: (-p[0], p[1]))
        if mynotprecious:
            act = 'd%d'%mynotprecious[0][1]
            return act
        myprecious = [ (card.number, i+1) for (i, card) in enumerate(game.current_hand.cards) ]
        myprecious.sort(key=lambda p: (-p[0], p[1]))
        act = 'd%d'%myprecious[0][1]
        return act
