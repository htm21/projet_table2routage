# *Tables de Routage,  un projet de 2ème année de Licence Informatique*

**NOM DES ÉTUDIANTS** : \
Ahmad HATOUM (22202060) - Francesco DI GENNARO (22205989)  



**URL DE DÉPÔT DU PROJET** : [https://github.com/htm21/projet_table2routage/]

## Installation

L'installation des différents modules est faite par l'utilisation de [pip](https://pip.pypa.io/en/stable/)  dans le terminal :
```bash
pip install module
```
Les modules nécessaires sont les suivants : tkinter, ctypes, platform, pyglet, itertools, os, pillow


# Les Objectifs du projet

Le but du projet est de réaliser une application qui permette principalement d’établir la table de routage de chaque nœud d’un réseau de 100 nœuds. Dans ce réseau, différents types de nœuds sont présents : Tier1 (les Backbones), Tier2 (les TransitOperator), Tier3 (les Operators) avec une liaison bien précise entre eux. 


# Les Différentes Étapes de notre projet

- Création des class permettant la modélisation des Nœuds du réseau, comprennant les Tier1, Tier2, Tier3.
- Création de liens entre chaque type niveau des opérateurs, et donc d'un Graphe.
- Mise en place d'une vérification de la connexité du Graphe : avec l'implémentation du parcours en profondeur. 
- La détermination des tables de routage des 100 nœuds présents dans le réseau.
- Reconstitution du plus court chemin entre 2 nœuds.
- Implémentation du code dans une interface graphique (tkinter)



# Comment comprendre la structure du projet ?

**Dossier "Modules"**  
Ce dossier contient tous les sous-fichiers permettant le fonctionnement du code, les différents fichiers sont importés dans d'autres pour permettre l'utilisation de leurs codes.  

**Fichier main.py**  
Ce fichier permet l'exécution de l'application, il rassemble le tout, simplement.


# ANNEXE
![image](https://github.com/htm21/projet_table2routage/assets/113848193/d5ed4377-61dc-40bc-867f-d2774c4e31a0)
![image](https://github.com/htm21/projet_table2routage/assets/113848193/81f82954-fd87-462f-8fe1-61ab85444d8c)
