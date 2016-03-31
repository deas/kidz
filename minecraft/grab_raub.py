#!/usr/bin/python
# --------------------------------------
#
#     Minecraft Python API
#        Grab Raub
#
# Dieses Skript platziert zufällig Gräber welche
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
        # Zufälliger x,z Ort
        x = random.randint(-120, 120)
        z = random.randint(-120, 120)
        # Ermittle Höhe des ersten "Nicht-Luft" Blockes in Spalte
        y = minecraft.getHeight(x, z) - 1

        # Teste gefundenen Block
        blocks = [block.SAND.id, block.DIRT.id, block.GRASS.id]
        if minecraft.getBlock(x, y, z) in blocks:
            # Ist nutzbar - Suche beenden
            suche = False

    position = (x, y, z)

    return position


def erzeuge_grab(position, größe, tiefe, material, schatz):
    # Erzeuge grab an einer Position mit einem Material
    x1 = position[0] + (größe / 2)
    y1 = position[1] - tiefe
    z1 = position[2] + (größe / 2)
    x2 = position[0] - (größe / 2)
    y2 = position[1] - tiefe - größe
    z2 = position[2] - (größe / 2)
    minecraft.setBlocks(x1, y1, z1, x2, y2, z2, material)
    minecraft.setBlocks(x1 - 1, y1 - 1, z1 - 1, x2 + 1, y2 + 1, z2 + 1, block.AIR.id)

    # Füege dem Grab Schatz an Position hinzu
    x = position[0]
    y = position[1] - (größe - 1) - tiefe
    z = position[2]
    minecraft.setBlock(position[0], position[1] - tiefe - größe + 1, position[2], schatz)
    # Gebe Position des Schatz Blockes zurück
    return [x, y, z]


def setze_marker(position, material):
    # Setze Marker über das Grab
    minecraft.setBlock(position[0], position[1] + 20, position[2], material)


def aktualisiere_schätze(schatz_liste):
    schätze = []

    for schatz in schatz_liste:
        position = schatz[0]
        größe = schatz[1]
        tiefe = schatz[2]
        x = position[0]
        y = position[1] - (größe - 1) - tiefe
        z = position[2]
        if minecraft.getBlock(x, y, z) == block.AIR.id:
            # Schatz verschwunden
            time.sleep(1)
        else:
            schätze.append(schatz)

    return schätze


# --------------------------------------
#
# Hier geht es los
#
# --------------------------------------

minecraft = minecraft_api.Minecraft.create()

random.seed

schatzliste = []

grab_zähler = 8

minecraft.postToChat("Lass uns Gräber ausrauben!!")

print("Setze " + str(grab_zähler) + " Gräber und Schätze")

for grabzahl in range(grab_zähler):
    grab_position = ermittle_grab_position()

    # Setze Marker in den Himmel
    setze_marker(grab_position, block.GLASS.id)
    # Bestimme Schatzposition
    schatz_position = erzeuge_grab(grab_position, 4, 3, block.STONE.id, block.GOLD_BLOCK.id)
    # Speichere Schatzposition
    schatzliste.append(schatz_position)

    print("Grab " + str(grabzahl) + " gesetzt bei  " + str(grab_position))

verbliebene_schätze = grab_zähler

minecraft.postToChat("Es sind noch " + str(verbliebene_schätze) + " Schätze zu finden")

while len(schatzliste) > 0:
    # Aktualisiere Schatzliste
    schatzliste = aktualisiere_schätze(schatzliste)
    time.sleep(1)
