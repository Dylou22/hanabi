# Hanabi project

Projet d'IN104 de 1ère année à l'ENSTA Paris
Le but est de créer une IA capable de jouer au jeu de plateau Hanabi, à partir d'un module python fourni contenant une implémentation du jeu ainsi qu'une IA **"Cheater"** capable de voir son propre jeu.

# Stratégie du chapeau

Nous avons choisi d'implémenter une IA capable de jouer en suivant la stratégie dite *du chapeau*: lorsqu'un joueur doit donner un indicce, il calcule un nombre pour chaque autre joueur correspondant à sa recommandation de jeu (jeu ou défausse), le traduit en un indice donnable en jeu. Les autres joueurs sont capables de faire le calcul inverse et de déduire le nombre qui leur est attribué.

## 1ère implémentation 

Nous avons négligé quelques éléments de l'algorithme décrit dans l'article décrivant la stratégie dans cette version beta:
-non prise en compte des cartes "indispensables" (i.e. celles que les joueurs ne doivent pas défausser sous peine de ne pas pouvoir atteindre un score parfait) : dans le cas où le joueur n'a pas de cartes "mortes" (dont le double a déjà été joué) dans la main lorsqu'il doit défausser, il défausse alors sa 1ère carte
-nous avons décidé de fournir son nombre à chaque joueur, plutôt que d'écrire le calcul du décryptage juste après, ce qui nous semblait trop artificiel et peu intéressant.

### Stratégie

Afin de pouvoir décoder les indices, nous avons ajouté des attributs dans la classe **Card**:
1. "recommanded" : vaut **False** par défaut. Lorsque le joueur décrypte un indice qui lui recommande de jouer la carte, l'attribut passe à **True**.
2. "risky" : vaut **False** par défaut. Dès qu'un joueur joue une carte, que ce soit avec succès ou non, toutes les autres cartes déjà recommandées dans les mains des joueurs deviennent alors risquées : l'argument passe à **True**. Si la carte est recommandée à nouveau, l'attribut redevient **False**.
3. "dead" : vaut **False** par défaut. Lorsque le joueur décrypte un indice qui lui recommande de défausser la carte, l'attribut passe à **True**. Si jamais on lui recommande de jouer la carte par la suite, l'attribut redevient **False**.

On peut ainsi constituer une liste des cartes que le joueur devrait jouer (*recommanded == True and risky == False*), une liste que le joueur peut jouer si il y a peu de jetons rouges déjà en jeu (*recommanded == True and risky == True*) et une liste des cartes que le joueur devrait défausser (*dead == True*). Le calcul du nombre associé à la main du joueur est donc trivial.

### Résulats

L'IA ne perd déjà plus aucune partie. Les scores sont compris entre 10 et 25, avec un maximum à 17. (1488 pour un échantillon de 10 000 parties). Ci-dessous, les résultats de 10 000 parties de la Beta et 10 000 parties du Cheater fourni.

![Cheater IA vs Chapeau Beta IA](https://github.com/Dylou22/hanabi/blob/DevGermain/test/Histogramme_Beta_sans_indispensables_VS_Cheater.png)


## 2è implémentation

Plutôt que d'implémenter totalement les cartes indispensables, on décide de sauver uniquement les 5, identifiés manuellement comme les cartes défaussées qui coûtent le plus de parties.
