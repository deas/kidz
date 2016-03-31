#!/usr/bin/python3
# --------------------------------------
#
#     Raspberry Pi Minecraft
#       Pyramiden erzeuten
#
# Erzeuge Pyramiden mit Minecraft
#
# Autor : Matt Hawkins
# Beitragender: Andreas Steffan
#
# Date   : 01/09/2014
#
# http://www.raspberrypi-spy.co.uk/
#
# --------------------------------------

# Importiere Standard Bibliotheken
import time
import math

# Importiere Minecraft Bibliotheken
import mcpi.minecraft as minecraft_api
import mcpi.block as block

# Block Definitionen
# Siehe http://www.raspberrypi-spy.co.uk/2014/09/raspberry-pi-minecraft-block-id-number-reference/ for more blocks
LUFT = 0
DRECK = 3
SAND = 12
SANDSTEIN = 24
GOLD = 41

minecraft = minecraft_api.Minecraft.create()


def erzeuge_pyramide(position_x, position_y, position_z, breite, basis, wand, block_oben):
    # Funktion um Pyramide bei x,y,z zu erzeugen.
    # Mit Breite und angegebenen Materialien

    minecraft.postToChat("Erzeuge Pyramide!")

    # Stelle sicher, dass Breite ungerade ist damit die Pyramide mit einem einzigen Block oben
    # endet
    if breite % 2 == 0:
        breite = breite + 1

    height = (breite + 1) / 2
    halbe_breite = int(math.floor(breite / 2))

    print("Spieler : {} {} {}".format(position_x, position_y, position_z))
    print("Größe : {} Höhe : {} Halbebreite : {}".format(breite, height, halbe_breite))

    # Erzeuge Basis der Pyramide
    print("Erzeuge Basis")
    minecraft.setBlocks(position_x - halbe_breite - 2, position_y - 2, position_z - halbe_breite - 2, position_x + halbe_breite + 2, position_y - 2, position_z + halbe_breite + 2,
                        DRECK)
    minecraft.setBlocks(position_x - halbe_breite - 2, position_y - 1, position_z - halbe_breite - 2, position_x + halbe_breite + 2, position_y - 1, position_z + halbe_breite + 2,
                        basis)

    # Erzeuge Pyramide
    print("Erzeuge Pyramide")
    for y in range(position_y, position_y + height):
        minecraft.setBlocks(position_x - halbe_breite, y, position_z - halbe_breite, position_x + halbe_breite, y, position_z + halbe_breite, wand)
        halbe_breite = halbe_breite - 1

    # Wechsel zu Spitzenblock
    print("Welchsel zu top block")
    minecraft.setBlock(position_x, position_y + height - 1, position_z, block_oben)

    print("Positioniere Spieler oben")
    minecraft.player.setPos(position_x, position_y + height, position_z)


# Setze Spieler Position
minecraft.player.setPos(0, 1, 0)
playerPos = minecraft.player.getPos()
playerPos = minecraft_api.Vec3(int(playerPos.x), int(playerPos.y), int(playerPos.z))

# Setze untere Hälfte Sandstein
minecraft.setBlocks(-128, 0, -128, 128, -128, 128, SANDSTEIN)

# Setze obere Hälfte Luft
minecraft.setBlocks(-128, 1, -128, 128, 128, 128, LUFT)

# Erzeuge Pyramiden
erzeuge_pyramide(0, 1, 0, 51, SANDSTEIN, SANDSTEIN, GOLD)

erzeuge_pyramide(-40, 1, 40, 21, SANDSTEIN, SANDSTEIN, SANDSTEIN)
erzeuge_pyramide(-40, 1, -40, 21, SANDSTEIN, SANDSTEIN, SANDSTEIN)
erzeuge_pyramide(40, 1, 40, 21, SANDSTEIN, SANDSTEIN, SANDSTEIN)
erzeuge_pyramide(40, 1, -40, 21, SANDSTEIN, SANDSTEIN, SANDSTEIN)

erzeuge_pyramide(0, 1, 45, 31, SANDSTEIN, SANDSTEIN, SANDSTEIN)
erzeuge_pyramide(0, 1, -45, 31, SANDSTEIN, SANDSTEIN, SANDSTEIN)
erzeuge_pyramide(45, 1, 0, 31, SANDSTEIN, SANDSTEIN, SANDSTEIN)
erzeuge_pyramide(-45, 1, 0, 31, SANDSTEIN, SANDSTEIN, SANDSTEIN)
