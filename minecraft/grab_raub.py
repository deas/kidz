#!/usr/bin/python
# --------------------------------------
#
#     Minecraft Python API
#        Grab Raub
#
# Dieses Skript platziert zufaellig Graeber welche
# der Spieler finden soll.
#
# Autor : Matt Hawkins
# Betragender: Andreas Steffan
#
# Date   : 23/06/2016
#
# http://www.raspberrypi-spy.co.uk/
#
# --------------------------------------

# Importier Minecraft Bibliotheken
import mcpi.minecraft as minecraft_api
import mcpi.block as block
import random
import time


# --------------------------------------
# Definiere Funktionen
# --------------------------------------

def ermittle_grab_position():
    # Find Ort für Grab
    suche = True
    while suche == True:
        # Zufaelliger x,z Ort
        x = random.randint(-120, 120)
        z = random.randint(-120, 120)
        # Ermittle Hoehe des ersten "Nicht-Luft" Blockes in Spalte
        y = minecraft.getHeight(x, z) - 1

        # Teste gefundenen Block
        blocks = [block.SAND.id, block.DIRT.id, block.GRASS.id]
        if minecraft.getBlock(x, y, z) in blocks:
            # Ist nutzbar - Suche beenden
            suche = False

    position = (x, y, z)

    return position


def erzeuge_grab(position, groesse, tiefe, material, schatz):
    # Erzeuge ein Grab an einer Position mit einem Material
    x1 = position[0] + (groesse / 2)
    y1 = position[1] - tiefe
    z1 = position[2] + (groesse / 2)
    x2 = position[0] - (groesse / 2)
    y2 = position[1] - tiefe - groesse
    z2 = position[2] - (groesse / 2)
    minecraft.setBlocks(x1, y1, z1, x2, y2, z2, material)
    minecraft.setBlocks(x1 - 1, y1 - 1, z1 - 1, x2 + 1, y2 + 1, z2 + 1, block.AIR.id)

    # Fuege dem Grab Schatz an Position hinzu
    x = position[0]
    y = position[1] - (groesse - 1) - tiefe
    z = position[2]
    minecraft.setBlock(position[0], position[1] - tiefe - groesse + 1, position[2], schatz)
    # Gebe Position des Schatz Blockes zurück
    return [x, y, z]


def setze_marker(position, material):
    # Setze Marker ueber das Grab
    minecraft.setBlock(position[0], position[1] + 20, position[2], material)


def aktualisiere_schaetze(schatz_liste):
    schaetze = []

    for schatz in schatz_liste:
        position = schatz[0]
        groesse = schatz[1]
        tiefe = schatz[2]
        x = position[0]
        y = position[1] - (groesse - 1) - tiefe
        z = position[2]
        if minecraft.getBlock(x, y, z) == block.AIR.id:
            # Schatz verschwunden
            time.sleep(1)
        else:
            schaetze.append(schatz)

    return schaetze


# --------------------------------------
#
# Hier geht es los
#
# --------------------------------------

minecraft = minecraft_api.Minecraft.create()

random.seed

schatzliste = []

grab_zaehler = 8

minecraft.postToChat("Lass uns Graeber ausrauben!!")

print("Setze " + str(grab_zaehler) + " Graeber und Schaetze")

for grabzahl in range(grab_zaehler):
    grab_position = ermittle_grab_position()

    # Setze Marker in den Himmel
    setze_marker(grab_position, block.GLASS.id)
    # Bestimme Schatzposition
    schatz_position = erzeuge_grab(grab_position, 4, 3, block.STONE.id, block.GOLD_BLOCK.id)
    # Speichere Schatzposition
    schatzliste.append(schatz_position)

    print("Grab " + str(grabzahl) + " gesetzt bei  " + str(grab_position))

verbliebene_schaetze = grab_zaehler

minecraft.postToChat("Es sind noch " + str(verbliebene_schaetze) + " Schaetze zu finden")

while len(schatzliste) > 0:
    # Aktualisiere Schatzliste
    schatzliste = aktualisiere_schaetze(schatzliste)
    time.sleep(1)
