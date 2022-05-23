#!/usr/bin/env python3

from timeit import timeit
from sys import argv
from geo.point import Point
import math as m
from random import uniform
import matplotlib.pyplot as plt

def load_instance(filename):
    """
    loads .mnt file.
    returns list of points.
    """
    with open(filename, "r") as instance_file:
        points = [Point((float(p[0]), float(p[1]))) for p in (l.split(',') for l in instance_file)]
    return points


def fct(g1, g2): #g1 = [distance_min, couple de point de la distance min, points de l'ensemble]
    P = [g1[2][i] for i in range(len(g1[2]))] + [g2[2][i] for i in range(len(g2[2]))]
    if g1[0] < g2[0]:
        delta = g1[0]
        couple1 = g1[1]
    delta = g2[0]
    couple1 = g2[1]
    m = P[len(P)//2] #milieu
    Q = []
    for p in P:
        if m.coordinates[0]-delta <= p.coordinates[0] <= m.coordinates[0]+delta:
            Q.append(p)
    tri_fusion(Q, 1) #tri par ordonnees
    if len(Q)<=1: # si il y un point au milieu il fait forcement partie de g1 ou de g2
        return [delta, couple1, P]
    delta_prime =  Q[0].distance_to(Q[1])
    couple2 = [Q[0], Q[1]]
    # suffit de faire avec les 7suivants
    for i in range(0, len(Q)):
        x=min(len(Q), i+8)
        for j in range(i+1, x):
            if Q[i].distance_to(Q[j]) < delta_prime:
                delta_prime = Q[i].distance_to(Q[j])
                couple2 = [Q[i], Q[j]]
    if delta < delta_prime:
        return [delta, couple1, P]
    return [delta_prime, couple2, P]

def recherche_naive(P):
    n = len(P)
    x = P[1].coordinates[0] - P[0].coordinates[0]
    y = P[1].coordinates[1] - P[0].coordinates[1]
    F = [Point((P[0].coordinates[0], P[0].coordinates[1])), Point((P[1].coordinates[0], P[1].coordinates[1]))]
    distance_mini = m.sqrt(x**2+y**2)
    for i in range(0, n):
        for j in range(i+1, n):
            x_cour = P[j].coordinates[0] - P[i].coordinates[0]
            y_cour = P[j].coordinates[1] - P[i].coordinates[1]
            if m.sqrt(x_cour**2+y_cour**2) < distance_mini:
                distance_mini = m.sqrt(x_cour**2+y_cour**2)
                F = [Point((P[i].coordinates[0], P[i].coordinates[1])), Point((P[j].coordinates[0], P[j].coordinates[1]))]
    return [distance_mini, F, P] #F = couple de points les plus proches, P = les 2 ou 3 points que l'on avait au départ

def reigne(P):  #ne pas oublier de trier p avant
    n = len(P)
    if n <= 3:
        return recherche_naive(P)
    else:
        A = [P[i] for i in range(n//2)]
        B = [P[i] for i in range(n//2, n)]
        return fct(reigne(A),reigne(B))



def tri_fusion(tableau, i):
    n = len(tableau)
    if n <= 1:
        return tableau
    else:
        milieu = len(tableau)//2
        gauche = tri_fusion(tableau[0:milieu], i)
        droite = tri_fusion(tableau[milieu:], i)
        return fusion(gauche, droite, i)

def fusion(tab_gauche, tab_droite, i):
    #i indique si on classe par abscisses (0) ou par ordonnees (1)
    if tab_gauche == []:
        return tab_droite
    if tab_droite == []:
        return tab_gauche
    if (tab_gauche[0]).coordinates[i] < (tab_droite[0]).coordinates[i]:
        return [tab_gauche[0]] + fusion(tab_gauche[1:], tab_droite, i)
    return [tab_droite[0]] + fusion(tab_gauche, tab_droite[1:], i)


def print_solution(points):
    """
    affiche la solution pour l'instance donnee
    """
    Px = sorted(points,key=lambda x: x.coordinates[0])
    S = reigne(Px)
    distance_mini = S[0]
    couple = S[1]
    print("distance mini:", distance_mini)
    print("couple de points:", couple)

def main():
    """
    ne pas modifier: on charge des instances donnees et affiches les solutions
    """
    for instance in argv[1:]:
        points = load_instance(instance)
        print_solution(points)



#Tests de performance

def points(n):
    liste_points = []
    for i in range (n):
        liste_points.append(Point([uniform(0,10), uniform(0,10)]))
    return liste_points

def print_solution_naive(points):
    """
    affiche la solution pour l'instance donnee
    """
    Px = recherche_naive(points)
    distance_mini = Px[0]
    couple = Px[1]
    print("distance mini:", distance_mini)
    print("couple de points:", couple)

def test_naif(nb_mesures): #Valeur de nb_mesures tronquée à la dizaine près
    liste_x = []
    liste_y = []
    for x_i in range(2, nb_mesures//10):
        liste_x.append(x_i*10)
        y_i = timeit(lambda: print_solution_naive(points(x_i*10)), number=1)
        liste_y.append(y_i)
    plt.plot(liste_x,liste_y)
    plt.xlim(0,2000)
    plt.ylim(0,1)
    plt.xlabel("Nombre de points n")
    plt.ylabel("Temps d'exécution, en secondes")
    plt.title("Courbe de performance pour le test naïf")
    plt.show()


def test_div_pour_reigne(nb_mesures):
    liste_x = []
    liste_y = []
    for x_i in range(2, nb_mesures//10):
        liste_x.append(x_i*10)
        y_i = timeit(lambda: print_solution(points(x_i*10)), number=1)
        liste_y.append(y_i)
    plt.plot(liste_x,liste_y)
    plt.xlim(0,10000)
    plt.ylim(0,1)
    plt.xlabel("Nombre de points n")
    plt.ylabel("Temps d'exécution, en secondes")
    plt.title("Courbe de performance pour le test diviser pour reigner")
    plt.show()


if __name__ == "__main__":
    main()
