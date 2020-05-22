# Hanabi project

Projet d'IN104 de 1ère année à l'ENSTA Paris
Le but est de créer une IA capable de jouer au jeu de plateau Hanabi, à partir d'un module python fourni contenant une implémentation du jeu ainsi qu'une IA **"Cheater"** capable de voir son propre jeu.

# Approche du projet et stratégie du chapeau

La prise en main du projet s'est faite non sans mal car nous avons eu des difficultés à voir toutes les possibilités qui s'offraient à nous. En effet, le code fourni était dense et se l'approprier a été assez long : vérifier la syntaxe de chaque élément que l'on veut utiliser, quel endroit du code correspond à quelle étape de jeu... Nous nous sommes donc intéressés dans un premier temps au déchiffrage de toutes les fonctions et classes importantes de l'algorithme.
Nous avons ensuite choisi d'implémenter une IA capable de jouer en suivant la stratégie dite *du chapeau* (1ère stratégie présentée dans la documentation) : lorsqu'un joueur doit donner un indice, il calcule un nombre pour chaque autre joueur correspondant à sa recommandation de jeu (jouer ou défausser), le traduit en un indice donnable en jeu. Les autres joueurs sont capables de faire le calcul inverse et de déduire le nombre qui leur est attribué. 
Nous avons cherché à rapidement obtenir une IA fonctionnelle en omettant plusieurs parties de l'algorithme afin d'ennsuite pouvoir la perfectionner.

## 1ère implémentation 

Nous avons négligé quelques éléments de l'algorithme décrits dans l'article décrivant la stratégie dans cette version beta:
-non prise en compte des cartes "indispensables" (i.e. celles que les joueurs ne doivent pas défausser sous peine de ne pas pouvoir atteindre un score parfait) : dans le cas où le joueur n'a pas de cartes "mortes" (dont le double a déjà été joué) dans la main lorsqu'il doit défausser, il défausse alors sa 1ère carte
-nous avons décidé de fournir son nombre à chaque joueur, plutôt que d'écrire le calcul du décryptage juste après, ce qui nous semblait trop artificiel et peu intéressant.

### Tests unitaires

Nous avons lancé d'innombrables parties à l'aide de '''game.turn()''' afin de tester la sortie de notre fonction '''nombre'''.
Par ailleurs, afin de débugger la 1ère itération de la liste '''mortes''' listant les cartes que le joueur pense défaussable au début de son tour, nous avons affiché son contenu ainsi que les attributs des cartes qu'elle contenait lors des parties que nous avons observées, et nous avons observé les attributs '''risky''' lorsque nous nous sommes rendus compte qu'ils ne passaient jamais à '''True'''. 

### Stratégie

Afin de pouvoir décoder les indices, nous avons ajouté des attributs dans la classe **Card**:
1. "recommanded" : vaut **False** par défaut. Lorsque le joueur décrypte un indice qui lui recommande de jouer la carte, l'attribut passe à **True**.
2. "risky" : vaut **False** par défaut. Dès qu'un joueur joue une carte, que ce soit avec succès ou non, toutes les autres cartes déjà recommandées dans les mains des joueurs deviennent alors risquées : l'argument passe à **True**. Si la carte est recommandée à nouveau, l'attribut redevient **False**.
3. "dead" : vaut **False** par défaut. Lorsque le joueur décrypte un indice qui lui recommande de défausser la carte, l'attribut passe à **True**. Si jamais on lui recommande de jouer la carte par la suite, l'attribut redevient **False**.

On peut ainsi constituer une liste des cartes que le joueur devrait jouer (*recommanded == True and risky == False*), une liste que le joueur peut jouer si il y a peu de jetons rouges déjà en jeu (*recommanded == True and risky == True*) et une liste des cartes que le joueur devrait défausser (*dead == True*). Le calcul du nombre associé à la main du joueur est donc trivial.

### Résulats

L'IA ne perd déjà plus aucune partie. Les scores sont compris entre 10 et 25, avec un maximum à 17. (1488 pour un échantillon de 10 000 parties). Ci-dessous, les résultats de 10 000 parties de la Beta et 10 000 parties du Cheater fourni.

![Cheater IA vs Chapeau Beta IA](https://github.com/Dylou22/hanabi/blob/DevDylan/test/Histogramme_Beta_sans_indispensables_VS_Cheater.png)


## 2è implémentation

Les cartes indispensables ont été implémentées à la fin de la fonction *nombre*. Nous avons également mis à jour la manière de donner les indices : les indices de rang sont systématiquement des 5. Ainsi, on évite de les défausser.

# Résultat
On obtient en l'état une moyenne de 20.6. On peut dire que l'ajout des cartes indispensables.

![Chapeau Beta IA VS Chapeau Avec 5 Sauvés](https://github.com/Dylou22/hanabi/blob/DevDylan/VersionFinale.png)

# 3ème implémentation et resultats finaux
On a fini par atteindre un score moyen de 21,06. Le script '''test_ai_chapeau.py''' lance l'AI 10000 fois. Au vu de l'article on peut déjà comprendre qu'il manque certaines parties de l'algorithme car dans l'article 'the recommandation strategy" obtient une moyenne de 23. 

# Mauvaises idées
Nous avons remarqué qu'en fin de partie la condition *risky==True* qui empêche de jouer était un peu forte et que l'on se retrouvait avec un dernier tour où souvent personne ne jouait de carte. Nous avons donc rajouté une condition pour que les joueurs jouent quand même leur carte même si elle est risquée lorsque le deck est vide. Il s'est avéré que les resultats étaient similaires avec et sans cette condition. De plus en toute fin de partie on a remarqué que la conditions risky==True empêche souvent les joueurs de jouer au dernier tour. On a essayé de faire jouer les joueurs au même si cela était risqué au dernier tour mais es résultats ont été sensiblement les mêmes (voir moins bons). 

# Piste d'améliorations et idées non réalisées 
En l'état actuel du projet, les indices "réels" que le joueur donne sont toujours les mêmes, c'est à dire si l'algorithme dit que le joueur doit donner un indice sur la couleur à un autre joueur il donnera toujours la couleur rouge (pour le rang de la carte ce sera 1). En ne nous servant que de l'indice "meta" et en négligeant l'indice "réel", on perd donc de l'information (même si elle n'est pas primordiale pour l'algorithme). Si ces indices étaient données avec plus de discernement, ils pourraient se révéler utiles surtout en fin de partie.
