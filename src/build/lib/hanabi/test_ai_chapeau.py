import hanabi
from ai import Robot

game = hanabi.Game(5)  # 2 players
ai = Robot(game)

# pour jouer toute une partie
game.ai = ai
game.run()