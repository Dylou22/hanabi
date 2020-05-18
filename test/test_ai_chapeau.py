import hanabi
from hanabi.ai import *
import numpy as np
import matplotlib.pyplot as plt
plt.close()
H = np.zeros(26)
I = np.zeros(26)
for i in range (10000):
    game = hanabi.Game(5)  # 2 players
    ai = Robot(game)
    # pour jouer toute une partie
    game.quiet = True
    game.ai = ai
    score = game.run()
    H[score]+=1
# for i in range(1000):
#     game = hanabi.Game(5)  # 2 players
#     ai = Cheater(game)
#     # pour jouer toute une partie
#     game.quiet = True
#     game.ai = ai
#     score = game.run()
#     I[score]+=1
print(H)
plt.plot(H)
# plt.plot(I)
# plt.show()
H_mortes_beta = [0,0,0,0,0,0,0,0,0,0,4,13,69,271,586,1061,1423,1488,1358,1107,915,700,515,271,158,61]
H_mortes_deuxpointszero = [0.000e+00,0.000e+00,0.000e+00,0.000e+00,0.000e+00,0.000e+00 ,0.000e+00,0.000e+00,0.000e+00,1.000e+00,4.000e+00,1.900e+01,7.900e+01,2.550e+02,6.470e+02,1.053e+03,1.391e+03,1.515e+03,1.310e+03,1.085e+03,8.800e+02,7.160e+02,5.300e+02,2.950e+02,1.720e+02,4.800e+01]
H_5_sauves = [0,0,0,0,0,0,0,0,0,0,0,0,0,2,15,74,254,616,1125,1454,1630,1317,1128,900,748,737]
H_c1_sauve = [0.000e+00,0.000e+00 ,0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00,0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 0.000e+00, 1.000e+00, 5.000e+00,1.800e+01, 7.100e+01, 2.560e+02, 5.860e+02, 1.116e+03, 1.511e+03, 1.548e+03,1.395e+03, 1.111e+03, 8.620e+02, 7.610e+02, 7.590e+02]
plt.plot(H_mortes_beta)
plt.plot(H_mortes_deuxpointszero)
plt.plot(H_5_sauves)
plt.show()
