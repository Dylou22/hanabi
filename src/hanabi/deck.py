"""
Hanabi deck and game engine module.

See also the program hanabi.

.. autosummary::
   Card
   Hand
   Deck
   Game
"""

import os
import copy
import random
import readline  # this greatly improves `input`

from enum import Enum
from enum import unique

from hanabi import ascii_art
from hanabi import ai


@unique
class Color(Enum):
    "Card colors. Int values correspond to xterm's."
    Red = 31
    Blue = 34
    Green = 32
    White = 37
    Yellow = 33
    # Red = 41
    # Blue = 44
    # Green = 42
    # White = 47
    # Yellow = 43
#    Multi = 6

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Color.'+self.name

    def colorize(self, *args):
        "Colorize and convert to str the given args."
        s = ' '.join(map(str, args))
        if os.name == 'posix':
            return '\033[%im'%self.value + s + '\033[0m'
        else:
            return s


class Card:
    "A hanabi card."
    def __init__(self, color=None, number=None):
        assert (1 <= number <= 5), "Wrong number"
        self.color = color
        self.number = number
        self.color_clue = False
        self.number_clue = False
         """
         Les attributs qui suivent indiquent le status des cartes au cours de la partie, selon les indices qui ont été donnés
         """
        self.recommanded = False
        self.risky = False
        self.dead = False
        

    def __str__(self):
        return (str(self.color)[0] + str(self.number))

    def __repr__(self):
        return ("Card(%r, %d)"%(self.color, self.number))

    def str_color(self):
        "Colorized string for this card."
        return self.color.colorize(str(self))

    def __eq__(self, c):
        """Return whether 2 cards are equal.
        Can compare 2 Card objects or their string value.
        """
        return str(self) == str(c)

    def str_clue(self):
        "What I know about this card."
        return (self.color_clue or '*') + (self.number_clue or '*')


class Hand:
    """A Hanabi hand, with n cards, drawn from the deck.
    Also used for the discard pile.
    """
    def __init__(self, deck, n=5):
        # TODO: see if it's easier to derive from list
        self.cards = []
        for i in range(n):
            self.cards.append(deck.draw())
        self._deck = deck  # not sure if I need it

    def __str__(self):
        return " ".join([c.str_color() for c in self.cards])

    def __repr__(self):
        return str(self)

    def str_clue(self):
        return " ".join([c.str_clue() for c in self.cards])

    def pop(self, i):
        "Pop a card from the hand, and draw a new one."
        if not 1 <= i <= len(self):
            raise ValueError("%d is not a valid card index."%i)
        i = i-1   # back to 0-based-indices
        card = self.cards.pop(i)
        try:
            self.cards.append(self._deck.draw())
        except IndexError:
            pass  # deck is empty
        return card

    def append(self, c): self.cards.append(c)

    def sort(self): self.cards.sort(key=str)

    def __len__(self): return len(self.cards)


class Deck:
    """
    A Hanabi deck of cards (50 cards).
    """
    # Rules for making decks:
    card_count = {1: 3, 2: 2, 3: 2, 4: 2, 5: 1}
    # Rules for dealing:
    cards_by_player = {2: 5, 3: 5, 4: 4, 5: 4}

    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
            for number, count in self.card_count.items():
                for color in list(Color):
                    for _ in range(count):
                        self.cards.append(Card(color, number))
        else:
            self.cards = cards

    def __str__(self):
        return " ".join([c.str_color() for c in self.cards])

    def __repr__(self):
        s = '['
        s += ", ".join(map(repr, self.cards))
        s += ']'
        return s

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        "Draw a card from the deck."
        return self.cards.pop(0)

    def deal(self, nhands):
        "Deal n hands and return them."
        hands = []
        for i in range(nhands):
            hands.append(Hand(self, self.cards_by_player[nhands]))
        return hands


class Game:
    """A game of Hanabi.

    Usage:

        >>> import hanabi
        >>> game = hanabi.Game(players=2)
        >>> game.run()    # users play a whole game

        >>> # if an AI is set, it will play the game automatically:
        >>> ai = hanabi.ai.Cheater(game)
        >>> game.ai = ai
        >>> game.run()

        >>> # For debugging, a single player turn can be played:
        >>> game = hanabi.Game(players=2)
        >>> game.turn()  # Alice will be asked to play
        >>> game.turn()  # and now Benji

        >>> # Same with an AI:
        >>> game = hanabi.Game(players=2)
        >>> ai = hanabi.ai.Cheater(game)
        >>> game.turn(ai)  # the ai will play just once
    """

    Players = ["Alice", "Benji", "Clara", "Dante", "Elric"]

    def __init__(self, players=2, multi=False):
        # Actions are functions that a player may do.
        # They should finish by a call to next_player, if needed.
        self.actions = {
            'd': self.discard,
            'p': self.play,
            'c': self.clue,
            'x': self.examine_piles,
            'l': self.load,
            '>': self.command,  # cheat-code !
            '?': (lambda x: self.log(ai.Cheater(self).play()))
        }
        self.reset(players, multi)
        self.quiet = False

    def log(self, *args, **kwargs):
        if self.quiet:
            pass
        else:
            print(*args, **kwargs)


    def reset(self, players=2, multi=False, cards=None):
        "Reset this game."
        if isinstance(players, int):
            assert(2 <= players <= 5)
            self.players = self.Players[:players]
        else:  # assume it's the list of players
            self.players = players

        self.deck = Deck(cards)
        if cards is None:
            self.deck.shuffle()

        # record starting deck and moves, for replay
        self.moves = []
        self.starting_deck = copy.deepcopy(self.deck)

        self.hands = self.deck.deal(len(self.players))

        self.current_player = None
        self.next_player()
        self.last_player = None  # will be set to the last player, to allow last turn

        self.discard_pile = Hand(None, 0)  # I don't give it the deck, so it can't draw accidentaly a card
        self.piles = dict(zip(list(Color), [0]*len(Color)))

        self.blue_coins = 8
        self.red_coins = 0
        self.ai = None
        """
        Cet attribut permet au joueur actif d'accéder à la somme modulo 8 des nombres
        associés aux mains des autres joueurs afin de donner l'indice correspondant
        """
        self.somme_joueurs = 0
        


    def turn(self, _choice=None):
        """
        Play one round: ask the player what she wants to do, then update the game.
        If _choice is not None, play it instead of asking.

        Note:

          If provided, _choice can be:
           - None: the human will be prompted
           - a (str), which is played
           - an AI object (we will play what its function play() suggests)
           - a list of actions, because I chose to
             record invalid actions too (and these loop within this file).
        """
        self.log()
        self.log(self.current_player_name,
                 "this is what you remember:",
                 self.current_hand.str_clue(),
                 #               self.current_hand,
                 "\n      this is what you see:")
        for player, hand in zip(self.players[1:], self.hands[1:]):
            self.log("%32s"%player, hand)
            self.log(" "*32, hand.str_clue())

        self.log("""What do you want to play?
        (d)iscard a card (12345)
        give a (c)lue (RBGWY 12345)
        (p)lay a card (12345)
        e(x)amine the piles""")

        # ai.Cheater(self).play()

        while True:
            if _choice is None:
                choice = input("hanabi> ")
                if choice.strip() == '':
                    continue
            elif isinstance(_choice, ai.AI):
                choice = _choice.play()
            elif isinstance(_choice, str):
                choice = _choice
            else:  # assume it is a list
                choice = _choice.pop(0)
                self.log('hanabi (auto)>', choice)
            # so here, choice is a 2 or 3 letters code:
            #  d2 (discard 2nd card)
            #  cR (give Red clue) ... will become cRA (give Red to Alice)
            #  p5 (play 5th card)

            self.moves.append(choice)
            try:
                self.actions[choice[0]](choice[1:])
                return
            except KeyError as e:
                self.log(e, "is not a valid action. Try again.")
            except (ValueError, IndexError) as e:
                self.log(e, "Try again")

    def add_blue_coin(self):
        if self.blue_coins == 8:
            raise ValueError("Already 8 blue coins. Can't get an extra one.")
        self.blue_coins += 1

    def remove_blue_coin(self):
        if self.blue_coins == 0:
            raise ValueError("No blue coin left.")
        self.blue_coins -= 1

    def add_red_coin(self):
        self.red_coins += 1
        if self.red_coins == 3:
            # StopIteration will stop the main loop!
            raise StopIteration()


    def discard(self, index):
        "Action: discard the given card from current hand (the first if index is an empty string)."
        try:
            if index.strip() == "":
                index = "1"
        except Exception:
            pass
        icard = int(index)
        self.add_blue_coin()
        try:
            card = self.current_hand.pop(icard)
        except ValueError:
            self.remove_blue_coin()
            raise
        self.discard_pile.append(card)
        self.discard_pile.sort()
        self.log(self.current_player_name, "discards", card.str_color(),
               "and now we have %d blue coins."%self.blue_coins)
        self.next_player()

    def play(self, index):
        "Action: play the given card."
        icard = int(index)
        card = self.current_hand.pop(icard)
        self.log(self.current_player_name, "tries to play", card, "... ", end="")
        """
        Update le statut des cartes déjà recommandées en recommandées + risquées si une carte est jouée entre temps
        """
        for i in range(5):
            for j in range(len(self.hands[i])):
                if self.hands[i].cards[j].recommanded ==True :
                    self.hands[i].cards[j].risky = True

        if (self.piles[card.color]+1 == card.number):
            self.piles[card.color] += 1
            self.log("successfully!")
            self.log(card.color.colorize(
                ascii_art.fireworks[self.piles[card.color]]))
            if self.piles[card.color] == 5:
                try:
                    self.add_blue_coin()
                except ValueError:  # it is valid to play a 5 when we have 8 coins. It is simply lost
                    pass
            #Après que le joueur ait joué avec succès, toutes les cartes recommandée deviennent risquées

        else:
            # misplay!
            self.discard_pile.append(card)
            self.log("That was a bad idea!")
            self.log(ascii_art.kaboom)
            self.add_red_coin()
        self.print_piles()
        self.next_player()


    def clue(self, clue):
        """Action: give a clue.

        clue[0] is within (12345RBGWY).
        By default, the clue is given to the next player (backwards compatibility with 2 payers games).
        If clue[1] is given it is the initial (ABCDE) or index (1234) of the target player.
        """

        hint = clue[0].upper()  # so cr is valid to clue Red
        if hint not in "12345RBGWY":
            raise ValueError("%s is not a valid clue."%hint)
        self.remove_blue_coin()  # will raise if no blue coin left

        try:
            target_index = clue[1]
            if target_index in 'ABCDE':
                short_names = [name[0] for name in self.players]
                target_index = short_names.index(target_index)
        except IndexError:
            target_index = 1
        target_index = int(target_index)
        if target_index == 0:
            raise ValueError("Cannot give a clue to yourself.")

        target_name = self.players[target_index]

        self.log(self.current_player_name, "gives a clue", hint, "to", target_name)
        """
        liste_nombre contient le nombre associé à l'indice qu'il faut donner à chaque joueur. Ce nombre est mis à jour après chaque indice donné
        """
        liste_nombre = [nombre(self,joueur) for joueur in range(5)]#Contient le nombre de chaque joueur après avoir donné un indice
        somme = sum(liste_nombre)
        self.somme_joueurs = (somme-liste_nombre[1])%8
        """
        Après avoir donné l'indice, les joueurs mettent à jour ce qu'ils savent de leurs cartes. Selon le nombre correspondant à leur main,
        ils mettent à jour le statut recommandé, risqué ou mort des cartes de leur jeu
        """
        for i in range(1,5):
            n_propre = liste_nombre[i]
            if n_propre == 0:
                self.hands[i].cards[0].recommanded = True
                self.hands[i].cards[0].risky = False
                self.hands[i].cards[0].dead = False
            if n_propre == 1:
                self.hands[i].cards[1].recommanded = True
                self.hands[i].cards[1].risky = False
                self.hands[i].cards[1].dead = False
            if n_propre == 2:
                self.hands[i].cards[2].recommanded = True
                self.hands[i].cards[2].risky = False
                self.hands[i].cards[2].dead = False
            if n_propre == 3:
                self.hands[i].cards[3].recommanded = True
                self.hands[i].cards[3].risky = False
                self.hands[i].cards[3].dead = False
            if n_propre == 4:
                self.hands[i].cards[0].dead = True
                self.hands[i].cards[0].recommanded = False
            if n_propre == 5:
                self.hands[i].cards[1].dead = True
                self.hands[i].cards[1].recommanded = False
            if n_propre == 6:
                self.hands[i].cards[2].dead = True
                self.hands[i].cards[2].recommanded = False
            if n_propre == 7:
                self.hands[i].cards[3].dead = True
                self.hands[i].cards[3].recommanded = False
               
        #  player = clue[1]  # if >=3 players
        for card in self.hands[target_index].cards:
            if hint in str(card):
                if hint in "12345":
                    card.number_clue = hint
                else:
                    card.color_clue = hint
        self.next_player()

    def examine_piles(self, *unused):
        "Action: look at the table."
        self.print_piles()

    def _bw_print_piles(self):
        self.log("    Discard:", self.discard_pile)
        for c in list(Color):
            self.log("%6s"%c, "pile:", self.piles[c])
        self.log("     Coins:", self.blue_coins, "blue,", self.red_coins, "red")

    def _color_print_piles(self):
        self.log("       Deck:", len(self.deck.cards))
        self.log("    Discard:", self.discard_pile)
        for c in list(Color):
            self.log(c.colorize("%6s"%c, "pile:", self.piles[c]))
        self.log("     Coins:", self.blue_coins, "blue,", self.red_coins, "red")

    def print_piles(self):
        self._color_print_piles()

    def next_player(self):
        """Switch to next player.

        Player 0 is *always* the current_player.
        """

        if self.current_player is None:   # called at game setup
            # I keep these two constants for the moment:
            self.current_player = 0
            self.other_player = 1
        else:
            # rotate players and hands
            self.hands.append(self.hands.pop(0))
            self.players.append(self.players.pop(0))

        self.current_player_name = '\033[1m%s\033[0m'%self.players[self.current_player]
        self.current_hand = self.hands[self.current_player]

        # other nice ideas: https://stackoverflow.com/questions/23416381/circular-list-iterator-in-python
        # itertools.cycle or players.append(pop(0))

    def command(self, args):
        "Action: Run a python command from Hanabi (yes, it is a cheat code: self is the current Game)."
        self.log('About to run `%s`'%args)
        try:
            exec(args)
        except Exception as e:
            self.log('Error:', e)
            # raise

    @property
    def score(self):
        return sum(self.piles.values())

    def run(self):
        try:
            last_players = list(self.players)
            while last_players:
                if len(self.deck.cards) == 0:
                    self.log()
                    self.log("--> Last turns:",
                             " ".join(last_players),
                             "may still play once.")
                    try:
                        last_players.remove(self.players[self.current_player])
                    except ValueError:
                        pass  # if Alice 'x', she is removed but plays again
                self.turn(self.ai)
                if self.score == 25:
                    raise StopIteration("it is perfect!")
            self.log("Game finished because deck exhausted")
        except (KeyboardInterrupt, EOFError, StopIteration) as e:
            self.log('Game finished because of', e)
            pass
        self.save('autosave.py')

        self.log("\nOne final glance at the table:")
        self.log(self.starting_deck)
        self.print_piles()
        #print("\nGoodbye. Your score is %d"%self.score)
        return(self.score)

    def save(self, filename):
        """Save starting deck and list of moves."""
        f = open(filename, 'w')
        f.write("""
players = %r
cards = %r
moves = %r
"""%(self.players,
     self.starting_deck,
     self.moves))
        # fixme: seems that a deck's repr is its list of cards?

    def load(self, filename):
        """Load a saved game, replay the moves.

        A saved game consists of the variables players, cards and moves.
        """
        f = open(filename)
        # in python3, it is tricky to modify a variable with exec:
        #   https://stackoverflow.com/questions/15086040/behavior-of-exec-function-in-python-2-and-python-3
        # need globals for the Card and Color definitions, and loaded-dict for returned values
        loaded = {}
        for l in f:
            exec(l, globals(), loaded)

        self.log('Loaded:', loaded)
        multi = False
        players = list(loaded['players'])
        cards = loaded['cards']
        moves = loaded['moves']

        self.reset(players, multi, cards)
        # for m in moves:
        #     self.turn(m)
        # was simpler, but infinity-looped when user made a mistake
        while moves:
            self.turn(moves)

def nombre(game,joueur):
   """
   Cette fonction calcule le nombre associé à la main d'un joueur. Elle renvoie un nombre entre 0 et 7
   qui correspond au coup que le joueur devrait faire : jouer ou défausser
   """
    
    main = game.hands[joueur].cards
    playable = [ (i+1, card.number) for (i, card) in
                enumerate(main)
                if game.piles[card.color]+1 == card.number ]

    #print(playable)
    #Ici on dispose de la main du joueur actuel, de l'état des piles, et des cartes jouables dans sa main
    #D'abord on étudie les cas où il y a des cartes jouables
    
    if playable != []:
        #print("playable = ",playable)
        #D'abord on cherche les 5 jouable
        cinq = None#L'indice d'un cinq jouable dans la main du joueur
        for i in range (len(playable)):
            if playable[i][1] == 5:
                carte = playable[i]
                return(carte[0]-1)
        min = playable[0][0]
        for i in range(len(playable)):
            if playable[i][0] <= min :
                min = playable[i][0]
                carte = playable[i]
        return(carte[0]-1)
    else:
        mortes = [ (i+1, card.number) for (i, card) in enumerate(main) if game.piles[card.color] >= card.number ]#Ne prend pas en compte les cartes indispensables
        if mortes !=[]:
            #print("mortes=",mortes)
            return(mortes[0][0]+3)
        else:#Ajouter cartes indispensables si ça marche
        #Une carte indispensable sera jouable mais ne l'est pas actuellement
        """
        On utilise une variante de l'algorithme proposé afin de sauver les 5 de la défausse: au lieu de conseiller de défausser la 1ère carte
        si il n'y a pas de cartes mortes, on conseille la 2è si la 1ère carte est un 5, la 3è si la 1ère et la 2è sont des 5, etc
        On regarde également si les cartes du joueur ont déjà été défaussées, ce qui constitue une version faible des cartes "indispensables"
        telles qu'elles sont définies dans l'article
        """
            defausse = game.discard_pile
            defausse_cartes = [ (i+1, card.number) for (i, card) in
                enumerate(defausse)]
            if main[0].number == 5 or main[0] in defausse.cards:
                print(main[0])
                print(defausse.cards)
                if main[1].number == 5 or main[1] in defausse.cards:
                    if main[2].number == 5 or main[2] in defausse.cards:
                        if main[3].number == 5 or main[3] in defausse.cards:
                            return(4)
                        return(7)
                    return(6)
                return(5)
            return(4)
    
        

if __name__ == "__main__":
    print("\nLet's start a new game")
    game = Game(5)
    print("Here are the hands:")
    print(game.hands)

    #game.run()
